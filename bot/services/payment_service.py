import requests
from loguru import logger
from pydantic import ValidationError
from requests import HTTPError
from requests.auth import HTTPBasicAuth
from telegram.constants import ParseMode
from telegram.ext import Application

from daos.payment_dao import PaymentDAO
from models.payment import Payment, PaymentStatus
from models.yookassa_payment_status import PaymentStatusDto
from models.yookassa_receipt_status import ReceiptStatusDto
from tg.utils.config import bot_config


async def fetch_receipt(payment_id: str) -> str:
    yookassa_base_url = "https://api.yookassa.ru/v3"
    auth = HTTPBasicAuth(bot_config.yookassa_shop_id, bot_config.yookassa_secret_key)
    payment_status_response = requests.get(
        f"{yookassa_base_url}/receipts?payment_id={payment_id}",
        auth=auth
    )
    payment_status_response.raise_for_status()
    payment_status_json = payment_status_response.json()
    payment_status = PaymentStatusDto(**payment_status_json)

    if not payment_status.items:
        raise ValueError("Payment status not found")

    receipt_id = payment_status.items[0].id
    receipt_status_response = requests.get(
        f"{yookassa_base_url}/receipts/{receipt_id}",
        auth=auth
    )
    receipt_status_response.raise_for_status()
    receipt_status_json = receipt_status_response.json()
    receipt_status = ReceiptStatusDto(**receipt_status_json)
    fiscal_provider_id = receipt_status.fiscal_provider_id

    return "{url}/{tin_numbers}/{fiscal_provider_id}/print".format(
        url="https://lknpd.nalog.ru/api/v1/receipt",
        tin_numbers=bot_config.tin_numbers,
        fiscal_provider_id=fiscal_provider_id,
    )


class PaymentService:
    def __init__(
            self,
            dao: PaymentDAO,
            app: Application
    ) -> None:
        self._dao = dao
        self._app = app

    async def create_payment(
            self,
            user_id: int,
            payment_id: str,
            message_id: int,
            amount: float,
            days: int
    ) -> Payment:
        payload = Payment(
            _id=payment_id,
            user_id=user_id,
            message_id=message_id,
            amount=amount,
            days=days
        )
        payment = await self._dao.create(payload)
        return payment

    async def confirm_payment(
            self,
            payment_id: str,
    ) -> Payment:
        payment = await self._dao.get(payment_id)
        if not payment:
            raise ValueError("Payment not found")
        if payment.status is PaymentStatus.succeeded:
            raise ValueError("Payment already succeeded")

        user_id = payment.user_id
        subscription_days = payment.days

        from services import get_user_service
        user_service = await get_user_service()
        await user_service.add_subscription_days(
            tg_id=user_id,
            days=subscription_days
        )

        payment.status = PaymentStatus.succeeded
        updated_payment = await self._dao.update(payment)

        user_id = payment.user_id
        message_id = payment.message_id
        await self._app.bot.edit_message_text(
            chat_id=user_id,
            message_id=message_id,
            text="""
*Спасибо за платёж!*
Ваша подписка активирована 🎉
            """,
            reply_markup=None,
            parse_mode=ParseMode.MARKDOWN
        )

        return updated_payment

    async def cancel_payment(
            self,
            payment_id: str,
    ) -> Payment:
        payment = await self._dao.get(payment_id)
        if not payment:
            raise ValueError("Payment not found")

        payment.status = PaymentStatus.canceled
        updated_payment = await self._dao.update(payment)
        return updated_payment

    async def try_fetch_all_receipts(self):
        payments = await self._dao.get_all_payments_without_receipt()
        for payment in payments:
            try:
                user_id = payment.user_id
                payment_id = payment.id
                receipt_url = await fetch_receipt(payment_id)
                await self._dao.attach_receipt_url(payment_id, receipt_url)
                await self._app.bot.send_message(
                    chat_id=user_id,
                    text=f"""
*Электронная копия чека*
📄 [Ссылка на чек]({receipt_url})
                    """,
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True,
                )
            except ValidationError:
                logger.exception("Invalid response")
            except ValueError:
                logger.warning("Receipt is not finished yet")
            except HTTPError:
                logger.exception("Error while fetching receipt")
