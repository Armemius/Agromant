from enum import Enum

from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime


class EventType(str, Enum):
    succeeded = "payment.succeeded"
    canceled = "payment.canceled"


class NotificationType(str, Enum):
    notification = "notification"


class Amount(BaseModel):
    value: str
    currency: str


class Recipient(BaseModel):
    account_id: str
    gateway_id: str


class PaymentMethod(BaseModel):
    type: str
    id: str
    saved: bool
    status: str
    title: str
    account_number: str


class PaymentObject(BaseModel):
    id: str
    status: str
    amount: Amount
    income_amount: Amount
    description: str
    recipient: Recipient
    payment_method: PaymentMethod
    captured_at: datetime
    created_at: datetime
    test: bool
    refunded_amount: Amount
    paid: bool
    refundable: bool
    metadata: Dict[str, Any]


class YookassaNotification(BaseModel):
    type: NotificationType
    event: EventType
    object: PaymentObject
