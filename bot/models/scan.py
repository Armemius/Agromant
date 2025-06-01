from datetime import datetime, timezone

from pydantic import BaseModel, PositiveFloat, model_validator, Field, PositiveInt


class PlantScan(BaseModel):
    user_id: PositiveInt = Field(
        ...,
        description="Telegram user-id of the user who made the request",
    )
    request_date: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
        description="UTC timestamp when the user registered",
    )
    images: PositiveInt = Field(
        default=0,
        description="Number of images in the request",
    )
    cost: PositiveFloat = Field(
        default=0.0,
        description="Request cost in RUB",
    )

    model_config = {
        "extra": "forbid",
        "populate_by_name": True,
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": 123456789,
                    "request_date": "2025-06-01T07:55:00Z",
                    "cost": 4.14,
                }
            ]
        },
    }
