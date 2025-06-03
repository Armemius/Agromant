from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from models.yookassa_common import ReceiptItemDto


class ReceiptStatusDto(BaseModel):
    id: str
    type: Optional[str]
    payment_id: Optional[str]
    status: Optional[str]
    registered_at: Optional[datetime]
    fiscal_provider_id: Optional[str]
    items: Optional[List[ReceiptItemDto]]
    tax_system_code: Optional[int]

    model_config = {
        "extra": "ignore"
    }
