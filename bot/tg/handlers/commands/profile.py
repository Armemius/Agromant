from telegram import Update
from telegram.ext import ContextTypes

from tg.decorators.command_handler import command_handler
from tg.utils.constants import PROFILE_KEYBOARD_BUTTON


@command_handler(name="profile", aliases=[PROFILE_KEYBOARD_BUTTON])
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.delete()