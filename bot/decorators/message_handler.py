from typing import Optional, Any

from loguru import logger
from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

from decorators.command_handler import get_alias_handler

message_handler_func: Optional[Any] = None


def message_handler(func):
    """Decorator that registers the default message handler."""

    global message_handler_func
    message_handler_func = func
    return func

async def message_processing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process incoming messages and route them to the appropriate handler."""
    message = update.message

    if message is not None:
        alias_handler = get_alias_handler(message.text)
        if alias_handler is not None:
            await alias_handler(update, context)
            return

    global message_handler_func
    if message_handler_func is not None:
        await message_handler_func(update, context)
        return

def register_message_handler(application):
    """
    Register the default message handler with the application.
    This function adds the message handler to the application.
    """

    application.add_handler(
        MessageHandler(
            filters.ChatType.PRIVATE & ~filters.COMMAND, message_processing
        )
    )
