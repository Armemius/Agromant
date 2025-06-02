
from fastapi import FastAPI, APIRouter

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
            print(data)
            payment_id = data.object.id
            payment_service = await get_payment_service()
            await payment_service.confirm_payment(payment_id)
