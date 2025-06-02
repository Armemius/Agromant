from typing import List, Optional

from pydantic import BaseModel

from models.yookassa_receipt_status import ReceiptStatusDto


class PaymentStatusDto(BaseModel):
    type: Optional[str]
    items: Optional[List[ReceiptStatusDto]]

    model_config = {
        "extra": "ignore"
    }
