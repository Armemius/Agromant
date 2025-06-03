from typing import Optional

from pydantic import BaseModel


class AmountDto(BaseModel):
    value: float
    currency: str

    model_config = {
        "extra": "ignore"
    }


class PaymentLineItemDto(BaseModel):
    description: Optional[str]
    quantity: Optional[float]
    amount: Optional[AmountDto]
    vat_code: Optional[int]
    payment_subject: Optional[str]
    payment_mode: Optional[str]

    model_config = {
        "extra": "ignore"
    }


class ReceiptItemDto(BaseModel):
    description: Optional[str]
    quantity: Optional[float]
    amount: Optional[AmountDto]
    vat_code: Optional[int]
    payment_subject: Optional[str]
    payment_mode: Optional[str]

    model_config = {
        "extra": "ignore"
    }
