from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from daos.payment_dao import PaymentDAO
from daos.scan_dao import PlantScanDAO
from daos.user_dao import TgUserDAO
from services.payment_service import PaymentService
from services.scan_service import PlantScanService
from services.user_service import TgUserService
from tg.utils.config import bot_config

logger.info("Wiring services to the application...")
mongo_uri = "mongodb://{user}:{password}@{host}:{port}".format(
    user=bot_config.mongo_username,
    password=bot_config.mongo_password,
    host=bot_config.mongo_host,
    port=bot_config.mongo_port
)
mongo = AsyncIOMotorClient(mongo_uri)
db = mongo[bot_config.mongo_database]

user_dao = TgUserDAO(db["tg_users"])
user_service = TgUserService(user_dao)

plant_scan_dao = PlantScanDAO(db["plant_scans"])
plant_scan_service = PlantScanService(plant_scan_dao)

payment_dao = PaymentDAO(db["payments"])
payment_service = PaymentService(payment_dao)
