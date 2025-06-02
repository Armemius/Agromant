from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from tg.decorators.callback_handler import gen_callback_data
from tg.decorators.command_handler import command_handler
from tg.utils.constants import SUBSCRIPTION_KEYBOARD_BUTTON, SUBSCRIPTION_CALLBACK


@command_handler(name="subscription", aliases=[SUBSCRIPTION_KEYBOARD_BUTTON])
async def subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.delete()

    layout = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "Купить на 7 дней: 99₽",
                callback_data=gen_callback_data(
                    SUBSCRIPTION_CALLBACK, {
                        "days": 7,
                        "amount": 99
                    }
                )
            ),
        ],
        [
            InlineKeyboardButton(
                "Купить на 14 дней: 169₽",
                callback_data=gen_callback_data(
                    SUBSCRIPTION_CALLBACK, {
                        "days": 14,
                        "amount": 169
                    }
                )
            ),
        ],
        [
            InlineKeyboardButton(
                "Купить на 30 дней: 290₽",
                callback_data=gen_callback_data(
                    SUBSCRIPTION_CALLBACK, {
                        "days": 30,
                        "amount": 290
                    }
                )
            ),
        ]
    ])

    await update.message.reply_text(
        """
✨ Подписка открывает полный доступ к анализу фотографий растений и рекомендациям
❗ Ограничение 30 запросов / неделя
        """,
        reply_markup=layout,
    )
