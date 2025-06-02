from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from models.payment import Payment


class PaymentDAO:
    def __init__(self, collection: AsyncIOMotorCollection):
        self._col = collection

    async def create(self, payload: Payment) -> Payment:
        await self._col.insert_one(payload.model_dump(by_alias=True))
        return Payment(**payload.model_dump(by_alias=True))

    async def update(self, payload: Payment) -> Payment:
        await self._col.update_one(
            {"_id": payload.id},
            {"$set": payload.model_dump(by_alias=True)}
        )
        return Payment(**payload.model_dump(by_alias=True))

    async def get(self, payment_id: str) -> Optional[Payment]:
        doc = await self._col.find_one({"_id": payment_id})
        if not doc:
            return None
        return Payment(**doc) if doc else None
