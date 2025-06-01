
from motor.motor_asyncio import AsyncIOMotorCollection

from models.scan import PlantScan


class PlantScanDAO:
    def __init__(self, collection: AsyncIOMotorCollection):
        self._col = collection

    async def create(self, payload: PlantScan) -> PlantScan:
        await self._col.insert_one(payload.model_dump(by_alias=True))
        return PlantScan(**payload.model_dump(by_alias=True))
