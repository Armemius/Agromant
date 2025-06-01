from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from tg.decorators.command_handler import command_handler
from tg.utils.constants import SUBSCRIPTION_KEYBOARD_BUTTON


@command_handler(name="subscription", aliases=[SUBSCRIPTION_KEYBOARD_BUTTON])
async def subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.delete()

    layout = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "Купить на 7 дней: 99₽",
                callback_data="subscription_7_days"
            ),
        ],
        [
            InlineKeyboardButton(
                "Купить на 14 дней: 169₽",
                callback_data="subscription_7_days"
            ),
        ],
        [
            InlineKeyboardButton(
                "Купить на 30 дней: 290₽",
                callback_data="subscription_7_days"
            ),
        ]
    ])

    await update.message.reply_text(
        """
Выберите срок подписки
        """,
        reply_markup=layout,
    )