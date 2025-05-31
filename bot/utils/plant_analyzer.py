import base64
from typing import List, Tuple

import cv2
import numpy as np
from openai import OpenAI

from utils.config import bot_config

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


def process_plant_analysis(images: List[Tuple[np.ndarray, str]]):
    response = client.responses.create(
        model="o4-mini",
        input=gen_request(images),
    )

    return response.output[1].content[0].text
