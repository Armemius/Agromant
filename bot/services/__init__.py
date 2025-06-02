from typing import Optional

from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from telegram.ext import Application

from daos.payment_dao import PaymentDAO
from daos.scan_dao import PlantScanDAO
from daos.user_dao import TgUserDAO
from services.payment_service import PaymentService
from services.scan_service import PlantScanService
from services.user_service import TgUserService

user_service: Optional[TgUserService] = None
payment_service: Optional[PaymentService] = None
plant_scan_service: Optional[PlantScanService] = None


async def get_user_service() -> TgUserService:
    global user_service
    if user_service is None:
        raise RuntimeError('User service not initialized')
    return user_service


async def get_payment_service() -> PaymentService:
    global payment_service
    if payment_service is None:
        raise RuntimeError('Payment service not initialized')
    return payment_service


async def get_plant_service() -> PlantScanService:
    global plant_scan_service
    if plant_scan_service is None:
        raise RuntimeError('Plant service not initialized')
    return plant_scan_service


async def wire_services(db: AsyncIOMotorDatabase, app: Application):
    global user_service, payment_service, plant_scan_service

    logger.info("Wiring services to the application...")

    user_dao = TgUserDAO(db["tg_users"])
    user_service = TgUserService(user_dao)

    plant_scan_dao = PlantScanDAO(db["plant_scans"])
    plant_scan_service = PlantScanService(plant_scan_dao)

    payment_dao = PaymentDAO(db["payments"])
    payment_service = PaymentService(payment_dao, app)
