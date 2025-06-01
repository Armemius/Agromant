from loguru import logger
from telegram import Update
from telegram.constants import ParseMode, ChatAction
from telegram.ext import ContextTypes

from services import plant_scan_service, user_service
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

    quota_check = await user_service.check_quota(
        tg_id=update.effective_user.id,
        images_count=len(images)
    )

    if not quota_check:
        await update.message.reply_text(
            """
К сожалению, у тебя закончились бесплатные запросы на анализ растений 🥺
Для продолжения использования бота, пожалуйста, купи подписку
            """,
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    message = await update.message.reply_text("🌱 Обрабатываю, подожди немного...")

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    try:
        input_tokens, output_tokens, text = await process_plant_analysis(images)
        await plant_scan_service.create_scan(
            user_id=update.effective_user.id,
            images_count=len(images),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )
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

    await user_service.consume_request(
        tg_id=update.effective_user.id,
        images_count=len(images)
    )

    await message.delete()
