import asyncio
import base64
from typing import List, Tuple

import cv2
import numpy as np
from loguru import logger
from openai import OpenAI, BadRequestError

from tg.utils.config import bot_config

client = OpenAI(
    api_key=bot_config.proxyai_api,
    base_url="https://api.proxyapi.ru/openai/v1",
)

with open("resources/plant_analysis/prompt.txt", "r", encoding="utf-8") as file:
    prompt = file.read()


def gen_base64_image(image: np.ndarray) -> str:
    success, jpeg_arr = cv2.imencode(".jpg", image, params=[cv2.IMWRITE_JPEG_QUALITY, 95])
    if not success:
        raise RuntimeError("JPEG encoding failed.")

    return "data:image/jpeg;base64," + base64.b64encode(jpeg_arr.tobytes()).decode(encoding="utf-8")


def gen_request(images: List[Tuple[np.ndarray, str]]) -> List:
    return [
        {
            "role": "system",
            "content": [{
                "type": "input_text",
                "text": prompt,
            }],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": gen_base64_image(x[0])
                } for x in images
            ]
        }

    ]


async def process_plant_analysis(images: List[Tuple[np.ndarray, str]]) -> Tuple[int, int, str]:
    tries = 5
    response = None
    while response is None:
        try:
            response = client.responses.create(
                model="o4-mini",
                input=gen_request(images)
            )
        except BadRequestError as e:
            await asyncio.sleep(0.5)
            logger.error(f"Error processing plant analysis: {e}, reties left: {tries}")
            tries -= 1
            if tries == 0:
                raise RuntimeError("Failed to process plant analysis after multiple attempts.")

    return (
        response.usage.input_tokens,
        response.usage.output_tokens,
        response.output[1].content[0].text
    )
