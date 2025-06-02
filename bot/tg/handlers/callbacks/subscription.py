from telegram import Update, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from services import payment_service
from tg.decorators.callback_handler import callback_handler
from tg.utils.constants import SUBSCRIPTION_CALLBACK
from tg.utils.yookassa import create_payment_url


@callback_handler(SUBSCRIPTION_CALLBACK)
async def remove_activity_callback(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        data: dict,
        query: CallbackQuery,
):
    user_id = update.effective_user.id
    payment_id, payment_url = create_payment_url(
        amount=data['amount'],
        description=f"Подписка на Telegram-бот Агромант на {data['days']} дней",
    )

    layout = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "Оплатить",
                url=payment_url,
            ),
        ],
    ])

    message = await context.bot.edit_message_text(
        message_id=query.message.message_id,
        chat_id=user_id,
        text=f"""
*Оплата бота*
Подписка на {data['days']} дней
        """,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=layout,
    )

    await payment_service.create_payment(
        user_id=user_id,
        message_id=message.message_id,
        payment_id=payment_id,
        amount=data['amount'],
        days=data['days'],
    )
    await query.answer()
