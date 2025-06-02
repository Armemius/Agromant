import json
import uuid
from typing import Tuple

from requests import post
from requests.auth import HTTPBasicAuth

from tg.utils.config import bot_config

with open("resources/payment.json.txt", "r", encoding="utf-8") as payment_info:
    payment = payment_info.read()


def create_payment_url(
        amount: float,
        description: str,
) -> Tuple[str, str]:
    current_payment_data = json.loads(
        payment.format(
            value=amount,
            description=description
        )
    )
    auth = HTTPBasicAuth(bot_config.yookassa_shop_id, bot_config.yookassa_secret_key)
    idempotence_key = uuid.uuid4().hex
    response = post(
        "https://api.yookassa.ru/v3/payments",
        auth=auth,
        json=current_payment_data,
        headers={
            "Idempotence-Key": idempotence_key,
        }
    )
    if response.status_code != 200:
        raise RuntimeError(f"Failed to create payment: {response.text}")

    payment_data = response.json()
    payment_id = payment_data["id"]
    url = payment_data["confirmation"]["confirmation_url"]

    return payment_id, url
