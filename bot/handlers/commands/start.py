import time

from telegram import Update
from telegram.constants import ParseMode, ChatAction
from telegram.ext import ContextTypes

from decorators.command_handler import command_handler


@command_handler(name="start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for /start command"""
    user_id = update.effective_user.id

    await context.bot.send_message(
        text="""
👋 Привет\\! Я *Агромант* — бот, который поможет тебе в уходе за растениями и в садоводстве
        """,
        chat_id=user_id,
        parse_mode=ParseMode.MARKDOWN_V2
    )

    await context.bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
    time.sleep(4)

    await context.bot.send_message(
        text="""
Иногда цветы и растения могут болеть и это всегда грустно\\. Но я помогу тебе определить, что с ними не так, и как это исправить
        """,
        chat_id=user_id,
        parse_mode=ParseMode.MARKDOWN_V2
    )

    await context.bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
    time.sleep(4)

    await context.bot.send_message(
        text="""
Для того чтобы подготовить рекомендации мне достаточно всего лишь парочки фотографий растения, которое тебя беспокоит
            """,
        chat_id=user_id,
        parse_mode=ParseMode.MARKDOWN_V2
    )