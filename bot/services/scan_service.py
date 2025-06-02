from datetime import datetime, timezone, timedelta
from typing import List


from daos.scan_dao import PlantScanDAO
from models.scan import PlantScan
from tg.utils.constants import PROXY_API_O4_MINI_INPUT_COST, PROXY_API_O4_MINI_OUTPUT_COST, REQUEST_QUOTA_PER_WEEK


class PlantScanService:
    def __init__(self, dao: PlantScanDAO):
        self._dao = dao

    async def create_scan(
            self,
            user_id: int,
            images_count: int,
            input_tokens: int,
            output_tokens: int,
            input_cost: float = PROXY_API_O4_MINI_INPUT_COST,
            output_cost: float = PROXY_API_O4_MINI_OUTPUT_COST
    ) -> PlantScan:
        now = datetime.now(tz=timezone.utc)
        total = (
                input_tokens / 1_000_000 * input_cost +
                output_tokens / 1_000_000 * output_cost
        )
        payload = PlantScan(
            user_id=user_id,
            images=images_count,
            request_date=now,
            cost=total,
        )
        scan = await self._dao.create(payload)
        return PlantScan(**scan.model_dump())

    async def count_all_request_images_last_week(
            self,
            user_id: int,
    ) -> int:
        return await self._dao.count_all_request_images_last_week(user_id)

    async def get_image_count_last_week_by_days(
            self,
            user_id: int,
    ) -> List[dict]:
        return await self._dao.get_image_count_last_week_by_days(user_id)

    async def check_subscription_quota(self, user_id: int, images_count: int) -> bool:
        requests_last_week = await self.count_all_request_images_last_week(user_id)
        return requests_last_week + images_count <= REQUEST_QUOTA_PER_WEEK

    async def get_recent_available_date(self, user_id) -> datetime:
        request_stats = await self.get_image_count_last_week_by_days(user_id)
        for stat in request_stats:
            images_count = stat["images"]
            if images_count > 0:
                date: datetime = stat["date"]
                return date + timedelta(days=7)
        return request_stats[-1]["date"] + timedelta(days=7)
