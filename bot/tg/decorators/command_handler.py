from typing import Any

from telegram.ext import (
    Application,
    CommandHandler
)
from loguru import logger

command_handlers: dict[str, CommandHandler] = {}
commands_map: dict[str, Any] = {}
alias_handlers: dict[str, Any] = {}


def command_handler(name: str, aliases: list = None):
    """
    Decorator to register a telegram bot command handler

    :param name: The name of the command (e.g., 'start', 'help')
    :param aliases: A list of aliases for the command (e.g., ['begin', 'go'])
    """
    def decorator(func):
        command_handlers[name] = CommandHandler(name, func)
        commands_map[name] = func
        if aliases:
            for alias in aliases:
                alias_handlers[alias] = func
        return func

    return decorator


def register_command_handlers(application: Application):
    """
    Register command handlers with the application.
    This function iterates over the command_handlers dictionary
    and adds each command handler to the application.
    """

    logger.debug("Registering command handlers")
    for cmd, handler in command_handlers.items():
        logger.debug(f"Registering command handler for '{cmd}'")
        application.add_handler(handler)



def get_alias_handler(alias: str):
    if alias in alias_handlers:
        return alias_handlers[alias]
    return None
