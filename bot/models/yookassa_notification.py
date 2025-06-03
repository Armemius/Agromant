from enum import Enum

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime


class EventType(str, Enum):
    succeeded = "payment.succeeded"
    canceled = "payment.canceled"


class NotificationType(str, Enum):
    notification = "notification"


class Amount(BaseModel):
    value: Optional[str] = None
    currency: Optional[str] = None


class Recipient(BaseModel):
    account_id: Optional[str] = None
    gateway_id: Optional[str] = None


class PaymentMethod(BaseModel):
    type: Optional[str] = None
    id: Optional[str] = None
    saved: Optional[bool] = None
    status: Optional[str] = None
    title: Optional[str] = None
    account_number: Optional[str] = None


class PaymentObject(BaseModel):
    id: Optional[str] = None
    status: Optional[str] = None
    amount: Optional[Amount] = None
    income_amount: Optional[Amount] = None
    description: Optional[str] = None
    recipient: Optional[Recipient] = None
    payment_method: Optional[PaymentMethod] = None
    captured_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    test: Optional[bool] = None
    refunded_amount: Optional[Amount] = None
    paid: Optional[bool] = None
    refundable: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


class YookassaNotification(BaseModel):
    type: NotificationType
    event: EventType
    object: PaymentObject
