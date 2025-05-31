import asyncio
import io
from collections import defaultdict
from typing import Optional, Tuple, List

import cv2
import numpy as np
from loguru import logger
from telegram import Update, Message
from telegram.ext import ContextTypes

album_cache = defaultdict(list)

async def download_photo(
        update: Update, context: ContextTypes.DEFAULT_TYPE, message: Optional[Message] = None
) -> Tuple[np.ndarray, str]:
    """Download the photo from Telegram and return the decoded image and its file_id."""
    if message is None:
        message = update.message

    photo = message.photo[-1]
    file = await context.bot.get_file(photo.file_id)

    buffer = io.BytesIO()
    await file.download_to_memory(buffer)
    buffer.seek(0)

    img_array = np.frombuffer(buffer.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img, photo.file_id


async def download_photos(
        update: Update, context: ContextTypes.DEFAULT_TYPE, messages: List[Message]
) -> List[Tuple[np.ndarray, str]]:
    """
    Download **all** photos attached to the Telegram message and return them as
    a list of (decoded_image, file_id) tuples.

    For a single photo Telegram always sends several PhotoSize objects
    (different resolutions).  If the user sent an album, this handler will still
    be called once per message in the album; each call downloads every size
    for that particular image.

    Returns
    -------
    List[Tuple[np.ndarray, str]]
        A list where each element is:
            0: the image as an OpenCV BGR ndarray
            1: the Telegram file_id for that PhotoSize
    """
    if not update.message or not messages:
        return []

    images: List[Tuple[np.ndarray, str]] = []

    for message in messages:
        images.append(await download_photo(update, context, message))

    return images


async def download_album(update: Update) -> List[Message]:
    """Download all photos in a media group (album) and return them as a list of Messages."""
    msg = update.message
    mgid = msg.media_group_id
    ALBUM_TIMEOUT = 0.5

    global album_cache

    if mgid is None:
        return []

    try:
        album_cache[mgid].append(msg)
        await asyncio.sleep(ALBUM_TIMEOUT)
        if album_cache[mgid][-1] is not msg:
            return []

        album = album_cache.pop(mgid)
        album.sort(key=lambda m: m.message_id)

        logger.info(f"Got {len(album)} photos")
        return album
    except Exception as e:
        logger.error(f"Error processing album: {e}")
        return []


async def get_message_images(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Optional[List[Tuple[np.ndarray, str]]]:
    """Get a list of images from the update."""

    msg = update.message
    mgid = msg.media_group_id

    if mgid is not None:
        try:
            album = await download_album(update)
            if not album:
                return None

            images = await download_photos(update, context, album)
        except Exception as e:
            logger.error(f"Error downloading album: {e}")
            return None
    elif update.message.photo:
        images = [await download_photo(update, context)]
    else:
        logger.warning("No photos found in the message.")
        return None

    if not images:
        logger.warning("No images downloaded.")
        return None

    return images