from daos.payment_dao import PaymentDAO
from models.payment import Payment, PaymentStatus


class PaymentService:
    def __init__(self, dao: PaymentDAO):
        self._dao = dao

    async def create_payment(
            self,
            user_id: int,
            payment_id: str,
            message_id: int,
            amount: float,
            days: int
    ) -> Payment:
        payload = Payment(
            id=payment_id,
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

        payment.status = PaymentStatus.succeeded
        updated_payment = await self._dao.update(payment)
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
