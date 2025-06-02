from enum import Enum

from loguru import logger
from telegram import Update
from telegram.constants import ParseMode, ChatAction
from telegram.ext import ContextTypes

from services import get_user_service, get_plant_service
from tg.decorators.message_handler import message_handler
from tg.utils.telegram_media_downloader import get_message_images


class QuotaStates(Enum):
    free_quota_expired = 0
    subscription_quota_expired = 1
    free_quota = 2
    subscription_quota = 3


def check_quota(
        valid_subscription: bool,
        free_quota_expired: bool,
        subscription_quota_expired: bool,
) -> QuotaStates:
    if valid_subscription:
        if not subscription_quota_expired:
            return QuotaStates.subscription_quota
        elif free_quota_expired:
            return QuotaStates.subscription_quota_expired
        else:
            return QuotaStates.free_quota
    else:
        if not free_quota_expired:
            return QuotaStates.free_quota
        else:
            return QuotaStates.free_quota_expired


@message_handler
async def default_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Default message handler for unhandled commands or messages."""

    user_id: int = update.effective_user.id
    if not update.message or not update.message.photo:
        await update.message.reply_text("""
🌱 Пришли мне фотографии растений, которые тебя беспокоят, и я помогу определить, что с ними не так
        """)
        return

    images = await get_message_images(update, context)

    if not images:
        return

    user_service = await get_user_service()
    plant_scan_service = await get_plant_service()

    valid_subscription = await user_service.has_valid_subscription(user_id)
    subscription_quota_check = await plant_scan_service.check_subscription_quota(
        user_id=user_id,
        images_count=len(images),
    )
    quota_check = await user_service.check_quota(
        tg_id=user_id,
        images_count=len(images)
    )

    quota_status = check_quota(
        valid_subscription=valid_subscription,
        subscription_quota_expired=not subscription_quota_check,
        free_quota_expired=not quota_check
    )

    match quota_status:
        case QuotaStates.free_quota_expired:
            await update.message.reply_text(
                text="""
К сожалению, у тебя закончились бесплатные запросы на анализ растений 🥺
Для продолжения использования бота, пожалуйста, купи подписку
                """
            )
            return
        case QuotaStates.subscription_quota_expired:
            date = await plant_scan_service.get_recent_available_date(user_id)
            await update.message.reply_text(
                text=f"""
К сожалению, у тебя закончились запросы на эту неделю 🥺
Новые запросы будут доступны {date.strftime('%d.%m.%Y')} 
                """
            )
            return

    message = await update.message.reply_text("🌱 Обрабатываю, подожди немного...")

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    try:
        input_tokens, output_tokens, text = 1, 1, "Amogus"  # await process_plant_analysis(images)
        await plant_scan_service.create_scan(
            user_id=user_id,
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

    if quota_status is QuotaStates.free_quota:
        await user_service.consume_request(
            tg_id=user_id,
            images_count=len(images)
        )

    await message.delete()
