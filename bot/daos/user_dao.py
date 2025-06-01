from typing import Optional

from bson import Int64
from motor.motor_asyncio import AsyncIOMotorCollection

from models.user import TgUser


class TgUserDAO:
    def __init__(self, collection: AsyncIOMotorCollection):
        self._col = collection

    async def create(self, payload: TgUser) -> TgUser:
        await self._col.insert_one(payload.model_dump(by_alias=True))
        return TgUser(**payload.model_dump(by_alias=True))

    async def get(self, tg_id: int) -> Optional[TgUser]:
        doc = await self._col.find_one({"_id": Int64(tg_id)})
        return TgUser(**doc) if doc else None

    async def check_quota(self, tg_id: int, amount: int = 1) -> bool:
        doc = await self._col.find_one({"_id": Int64(tg_id), "images_left": {"$gte": amount}})
        return doc is not None

    async def decrement_quota(self, tg_id: int, amount: int = 1) -> TgUser:
        doc = await self._col.find_one_and_update(
            {"_id": Int64(tg_id), "images_left": {"$gte": amount}},
            {"$inc": {"images_left": -amount}
             },
            return_document=True,
        )
        if not doc:
            raise RuntimeError("Not enough quota")
        return TgUser(**doc)
