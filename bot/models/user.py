from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, NonNegativeInt


class TgUser(BaseModel):
    id: PositiveInt = Field(..., alias="_id", description="Telegram user-id")
    registration_date: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
        description="UTC timestamp when the user registered",
    )
    images_left: NonNegativeInt = Field(
        default=0,
        description="How many free requests the user still has",
    )
    subscription_till: Optional[datetime] = Field(
        None,
        description="UTC timestamp until which the user is subscribed",
    )

    model_config = {
        "extra": "forbid",
        "populate_by_name": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 123456789,
                    "registration_date": "2025-06-01T07:55:00Z",
                    "images_left": 15,
                    "subscription_till": "2025-09-01T00:00:00Z",
                }
            ]
        },
    }
