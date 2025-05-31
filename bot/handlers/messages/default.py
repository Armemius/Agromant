from telegram import Update
from telegram.ext import ContextTypes

from decorators.message_handler import message_handler


@message_handler
async def default_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Default message handler for unhandled commands or messages."""

    user_id = update.effective_user.id

    await context.bot.send_message(
        text="PLACEHOLDER: Default message for unhandled commands or messages.",
        chat_id=user_id,
    )
