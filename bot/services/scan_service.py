from datetime import datetime, timezone

from pydantic.v1 import PositiveInt, PositiveFloat

from daos.scan_dao import PlantScanDAO
from models.scan import PlantScan
from tg.utils.constants import PROXY_API_O4_MINI_INPUT_COST, PROXY_API_O4_MINI_OUTPUT_COST


class PlantScanService:
    def __init__(self, dao: PlantScanDAO):
        self._dao = dao

    async def create_scan(
            self,
            user_id: PositiveInt,
            images_count: PositiveInt,
            input_tokens: PositiveInt,
            output_tokens: PositiveInt,
            input_cost: PositiveFloat = PROXY_API_O4_MINI_INPUT_COST,
            output_cost: PositiveFloat = PROXY_API_O4_MINI_OUTPUT_COST
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
