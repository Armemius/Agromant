from datetime import datetime, timedelta

from motor.motor_asyncio import AsyncIOMotorCollection

from models.scan import PlantScan


class PlantScanDAO:
    def __init__(self, collection: AsyncIOMotorCollection):
        self._col = collection

    async def create(self, payload: PlantScan) -> PlantScan:
        await self._col.insert_one(payload.model_dump(by_alias=True))
        return PlantScan(**payload.model_dump(by_alias=True))

    async def count_all_request_images_last_week(self, user_id: int) -> int:
        now = datetime.now()
        since = now - timedelta(days=7)

        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "request_date": {"$gte": since},
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_images": {"$sum": "$images"}
                }
            }
        ]

        cursor = self._col.aggregate(pipeline)
        result = await cursor.to_list(length=1)

        if result:
            return result[0].get("total_images", 0)
        return 0

    async def get_image_count_last_week_by_days(self, user_id: int):
        now = datetime.now()
        since = now - timedelta(days=7)

        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "request_date": {"$gte": since},
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$request_date"
                        }
                    },
                    "total_images": {"$sum": "$images"}
                }
            },
            {
                "$sort": {"_id": 1}
            }
        ]

        cursor = self._col.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        counts_by_day = {doc["_id"]: doc["total_images"] for doc in results}

        start_date = since.date()
        end_date = now.date()
        num_days = (end_date - start_date).days + 1

        output = []
        for i in range(num_days):
            day = start_date + timedelta(days=i)
            day_str = day.isoformat()
            output.append({
                "date": day,
                "images": counts_by_day.get(day_str, 0)
            })

        return output
