from loguru import logger
from telegram import Update
from telegram.constants import ParseMode, ChatAction
from telegram.ext import ContextTypes

from tg.decorators.message_handler import message_handler
from tg.utils.plant_analyzer import process_plant_analysis
from tg.utils.telegram_media_downloader import get_message_images


@message_handler
async def default_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Default message handler for unhandled commands or messages."""

    if not update.message or not update.message.photo:
        await update.message.reply_text("""
🌱 Пришли мне фотографии растений, которые тебя беспокоят, и я помогу определить, что с ними не так
        """)
        return

    images = await get_message_images(update, context)

    if not images:
        return

    message = await update.message.reply_text("🌱 Обрабатываю, подожди немного...")

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    try:
        text = await process_plant_analysis(images)
    except RuntimeError:
        logger.exception("Failed to process plant analysis")
        await update.message.reply_text(
            """
К сожалению, при обработке фотографий возникла ошибка. Пожалуйста, попробуй отправить фотографии ещё раз 😔
            """
        )
        return

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
    )
    await message.delete()
