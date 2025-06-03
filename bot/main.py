import asyncio
import importlib
import inspect
import pkgutil

from fastapi import FastAPI, APIRouter
from hypercorn import Config
from hypercorn.asyncio import serve
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from telegram.ext import Application

from api.payments import PaymentController
from services import wire_services, get_payment_service
from tg import handlers
from tg.decorators.callback_handler import register_callback_handlers
from tg.decorators.message_handler import register_message_handler
from tg.decorators.command_handler import register_command_handlers
from tg.utils.config import init_config, get_config


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


async def receipt_fetcher():
    while True:
        try:
            payment_service = await get_payment_service()
            await payment_service.try_fetch_all_receipts()
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.exception(f"Unhandled exception: {e}")


async def post_init(app: Application):
    await app.initialize()

    mongo_uri = "mongodb://{user}:{password}@{host}:{port}".format(
        user=get_config().mongo_username,
        password=get_config().mongo_password,
        host=get_config().mongo_host,
        port=get_config().mongo_port
    )
    mongo = AsyncIOMotorClient(mongo_uri)
    db = mongo[get_config().mongo_database]
    await wire_services(db, app)

    server = FastAPI()
    prefix_router = APIRouter(prefix="/api")
    config = Config()
    config.bind = "0.0.0.0:8000"
    PaymentController(prefix_router).register_routes()
    server.include_router(prefix_router)

    loop = asyncio.get_event_loop()
    loop.create_task(serve(server, config))
    loop.create_task(receipt_fetcher())


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
        .token(get_config().bot_key)
        .post_init(post_init)
        .concurrent_updates(1024)
        .write_timeout(999)
        .read_timeout(999)
        .pool_timeout(999)
        .connect_timeout(999)
    ).build()

    register_callback_handlers(app)
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

    if get_config().use_webhooks:
        logger.info("Using webhooks")
        app.run_webhook(
            allowed_updates=allowed_updates,
            webhook_url=get_config().webhook_url,
            url_path=get_config().webhook_path,
            max_connections=get_config().webhook_connections,
            listen="0.0.0.0",
            port=get_config().webhook_port,
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
