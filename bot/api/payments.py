from fastapi import FastAPI, APIRouter, HTTPException

from models.yookassa_notification import YookassaNotification
from services import get_payment_service


class PaymentController:
    def __init__(
            self,
            server: FastAPI | APIRouter = FastAPI(),
    ):
        self.server = server

    def register_routes(self):
        @self.server.post("/payment")
        async def process_payments(data: YookassaNotification):
            try:
                payment_id = data.object.id
                payment_service = await get_payment_service()
                await payment_service.confirm_payment(payment_id)
            except ValueError as ex:
                raise HTTPException(status_code=400, detail={
                    "ok": False,
                    "error": str(ex),
                })

            return {
                "ok": True,
            }
