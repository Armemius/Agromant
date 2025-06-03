from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class PaymentStatus(str, Enum):
    pending = "pending"
    succeeded = "succeeded"
    canceled = "canceled"


class Payment(BaseModel):
    id: str = Field(
        ...,
        alias="_id",
        description="Yookassa payment id"
    )
    user_id: PositiveInt = Field(
        ...,
        description="Telegram user id that made the payment"
    )
    message_id: int = Field(
        ...,
        description="Message id in Telegram where the payment was initiated"
    )
    days: int = Field(
        ...,
        description="Number of days the subscription is valid for"
    )
    payment_date: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
        description="UTC timestamp when the user registered",
    )
    amount: PositiveInt = Field(
        ...,
        description="Amount received in RUB"
    )
    status: PaymentStatus = Field(
        default=PaymentStatus.pending,
        description="Current payment status"
    )
    receipt_url: Optional[str] = Field(
        default=None,
        description="URL to receipt on nalog.gov.ru"
    )

    model_config = {
        "extra": "forbid",
        "populate_by_name": True,
        "json_schema_extra": {
            "examples": [
                {
                    "_id": "2fca9507-000f-5001-9000-1a3bdacdfd8b",
                    "payment_date": "2025-06-01T07:55:00Z",
                    "amount": 290,
                    "status": "succeeded",
                    "receipt_url": "https://www.nalog.gov.ru/receipt/2fca9507-000f-5001-9000-1a3bdacdfd8b"
                }
            ]
        },
    }
