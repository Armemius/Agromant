from datetime import datetime, timezone, timedelta

from daos.user_dao import TgUserDAO
from models.user import TgUser


class TgUserService:
    def __init__(self, dao: TgUserDAO):
        self._dao = dao

    async def register_if_needed(self, tg_id: int) -> TgUser:
        if user := await self._dao.get(tg_id):
            return TgUser(**user.model_dump())
        now = datetime.now(tz=timezone.utc)
        payload = TgUser(id=tg_id, registration_date=now, images_left=5)
        user = await self._dao.create(payload)
        return TgUser(**user.model_dump())

    async def images_left(self, tg_id: int) -> int:
        user = await self._dao.get(tg_id)
        if not user:
            return 0
        return user.images_left

    async def has_valid_subscription(self, tg_id: int) -> bool:
        user = await self._dao.get(tg_id)
        if not user:
            return False
        if user.subscription_till is None:
            return False
        return user.subscription_till >= datetime.now()

    async def get_subscription_expiration(self, tg_id: int) -> datetime | None:
        user = await self._dao.get(tg_id)
        if not user:
            return None
        return user.subscription_till

    async def consume_request(self, tg_id: int, images_count: int) -> TgUser:
        user = await self._dao.decrement_quota(tg_id, amount=images_count)
        return TgUser(**user.model_dump())

    async def check_quota(self, tg_id: int, images_count: int) -> bool:
        user = await self._dao.get(tg_id)
        if not user:
            return False
        return user.images_left >= images_count

    async def add_subscription_days(self, tg_id: int, days: int) -> None:
        user = await self._dao.get(tg_id)
        if not user:
            user = await self.register_if_needed(tg_id)

        if user.subscription_till is None or user.subscription_till < datetime.now():
            user.subscription_till = datetime.now()

        user.subscription_till = user.subscription_till + timedelta(days=days)
        await self._dao.update(user)
