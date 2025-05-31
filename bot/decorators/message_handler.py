from typing import Optional, Any

from loguru import logger
from telegram.ext import MessageHandler, filters

message_handler_func: Optional[Any] = None


def message_handler(func):
    """Decorator that registers the default message handler."""

    global message_handler_func
    message_handler_func = func
    return func


def register_message_handler(application):
    """
    Register the default message handler with the application.
    This function adds the message handler to the application.
    """

    global message_handler_func
    if message_handler:
        logger.debug("Registering default message handler")
        application.add_handler(MessageHandler(~filters.COMMAND, message_handler_func))
    else:
        logger.warning("No default message handler registered")
