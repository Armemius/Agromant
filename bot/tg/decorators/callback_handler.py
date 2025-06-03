import functools
import inspect
import json
import re
from typing import Optional
from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, ContextTypes
from loguru import logger

callback_handlers: dict[str, CallbackQueryHandler] = {}


def callback_handler(name: str):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(
                update: Update, context: ContextTypes.DEFAULT_TYPE, *a, **kw
        ):
            data = extract_data(update)
            query = update.callback_query

            return await func(update, context, data, query, *a, **kw)

        wrapper.__signature__ = inspect.signature(func)

        callback_handlers[name] = CallbackQueryHandler(
            wrapper, pattern=rf"^{re.escape(name)}"
        )

        return wrapper

    return decorator


def register_callback_handlers(app: Application):
    for handler in callback_handlers.values():
        logger.debug(
            f"Registering callback handler: {handler.callback.__name__}"
        )
        app.add_handler(handler)


def extract_data(update: Update):
    cq = update.callback_query
    if cq and cq.data:
        try:
            _, payload = cq.data.split("\n", 1)
            return json.loads(payload)
        except (ValueError, json.JSONDecodeError):
            logger.warning("bad callback payload")
    return None


def gen_callback_data(
        handler_name: str, callback_data: Optional[object] = None
) -> str:
    max_callback_length = 64

    if callback_data is None:
        callback_data = {}
    data = f"{handler_name}\n{json.dumps(callback_data)}"
    if len(data) > max_callback_length:
        logger.warning(
            f"Callback data exceeds {max_callback_length} characters. "
            "This may lead to errors!"
        )
    return data
