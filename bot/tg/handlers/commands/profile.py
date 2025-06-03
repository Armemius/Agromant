from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from services import get_user_service
from tg.decorators.command_handler import command_handler
from tg.utils.constants import PROFILE_KEYBOARD_BUTTON


@command_handler(name="profile", aliases=[PROFILE_KEYBOARD_BUTTON])
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id: int = update.effective_user.id
    await update.message.delete()
    user_service = await get_user_service()

    await update.message.reply_text(
        f"""
*Ваш профиль*
*ID*: {user_id}
*Имя*: {update.effective_user.first_name}
{
        f"*Подписка до*: {(await user_service.get_subscription_expiration(user_id)).strftime('%d.%m.%Y')}"
        if await user_service.has_valid_subscription(user_id)
        else "*Подписка*: не активна"
        }
{
        f"*Бесплатных запросов*: {await user_service.images_left(user_id)}"
        if await user_service.images_left(user_id) > 0 else ""
        }
""",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
