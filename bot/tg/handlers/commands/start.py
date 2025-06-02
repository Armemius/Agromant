import time

from telegram import Update, ReplyKeyboardMarkup
from telegram.constants import ParseMode, ChatAction
from telegram.ext import ContextTypes

from services import get_user_service
from tg.decorators.command_handler import command_handler
from tg.utils.constants import (
    PROFILE_KEYBOARD_BUTTON,
    SUBSCRIPTION_KEYBOARD_BUTTON,
    HELP_KEYBOARD_BUTTON,
    SUPPORT_KEYBOARD_BUTTON
)


@command_handler(name="start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /start command"""
    user_id = update.effective_user.id
    user_service = await get_user_service()
    await user_service.register_if_needed(user_id)

    await update.message.reply_text(
        text="""
👋 Привет\\! Я *Агромант* — бот, который поможет тебе в уходе за растениями и в садоводстве
        """,
        parse_mode=ParseMode.MARKDOWN_V2
    )

    await update.message.delete()

    await context.bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
    time.sleep(4)

    await update.message.reply_text(
        text="""
Иногда цветы и растения могут болеть и это всегда грустно\\. Но я помогу тебе определить, что с ними не так, и как это исправить
        """,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await context.bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
    time.sleep(4)

    layout = ReplyKeyboardMarkup(
        keyboard=[
            [
                PROFILE_KEYBOARD_BUTTON,
            ],
            [
                HELP_KEYBOARD_BUTTON,
                SUBSCRIPTION_KEYBOARD_BUTTON
            ],
            [
                SUPPORT_KEYBOARD_BUTTON
            ]
        ],
        resize_keyboard=True,
        is_persistent=False,
        one_time_keyboard=False,
        input_field_placeholder="Отправь фото в чат..."
    )

    await update.message.reply_text(
        text="""
Для того чтобы начать мне достаточно всего лишь парочки фотографий растения, которое тебя беспокоит
            """,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=layout
    )
