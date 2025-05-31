import asyncio
import io
from collections import defaultdict
from typing import Optional, Tuple, List

import cv2
import numpy as np
from loguru import logger
from telegram import Update, Message
from telegram.constants import ParseMode, ChatAction
from telegram.ext import ContextTypes

from decorators.message_handler import message_handler
from utils.plant_analyzer import process_plant_analysis
from utils.telegram_media_downloader import download_album, get_message_images


@message_handler
async def default_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Default message handler for unhandled commands or messages."""

    if not update.message or not update.message.photo:
        await update.message.reply_text("""
🌱 Пришли мне фотографии растений, которые тебя беспокоят, и я помогу определить, что с ними не так
        """)
        return

    images = await get_message_images(update, context)

    if not images:
        return

    message = await update.message.reply_text("🌱 Обрабатываю, подожди немного...")

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    text = process_plant_analysis(images)

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
    )
    await message.delete()
