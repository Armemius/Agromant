import importlib
import inspect
import pkgutil

from loguru import logger

from tg import handlers
from tg.decorators.message_handler import register_message_handler
from tg.decorators.command_handler import register_command_handlers
from tg.utils.config import init_config, bot_config


def load_all_modules():
    for loader, module_name, is_pkg in pkgutil.walk_packages(
            handlers.__path__, handlers.__name__ + "."
    ):
        module = importlib.import_module(module_name)
        for _ in inspect.getmembers(module):
            pass

def init():
    """
    Initialize the bot by loading all command modules and setting up the configuration.
    """
    logger.info("Initializing Agromant bot...")
    load_all_modules()
    init_config()
    logger.info("Agromant bot initialized successfully")


def start_telegram_bot():
    """
    Start the Telegram bot application.
    This function sets up the application, registers command handlers,
    and starts the bot.
    """
    from telegram.ext import ApplicationBuilder

    logger.info("Starting Telegram bot...")

    app = (
        ApplicationBuilder()
        .token(bot_config.bot_key)
        .concurrent_updates(1024)
        .write_timeout(999)
        .read_timeout(999)
        .pool_timeout(999)
        .connect_timeout(999)
    ).build()

    register_command_handlers(app)
    register_message_handler(app)

    allowed_updates = [
        "message",
        "edited_message",
        "channel_post",
        "edited_channel_post",
        "inline_query",
        "chosen_inline_result",
        "callback_query",
        "shipping_query",
        "pre_checkout_query",
        "poll",
        "poll_answer",
        "my_chat_member",
        "chat_member",
        "chat_join_request",
        "web_app_data"
    ]

    if bot_config.use_webhooks:
        logger.info("Using webhooks")
        app.run_webhook(
            allowed_updates=allowed_updates,
            webhook_url=bot_config.webhook_url,
            url_path=bot_config.webhook_path,
            max_connections=bot_config.webhook_connections,
            listen="0.0.0.0",
            port=bot_config.webhook_port,
            drop_pending_updates=False,
        )
    else:
        logger.info("Using long polling")
        app.run_polling(
            allowed_updates=allowed_updates,
            drop_pending_updates=False,
            timeout=10,
        )


def main():
    logger.info("Launching Agromant bot...")
    init()
    start_telegram_bot()


if __name__ == "__main__":
    main()
