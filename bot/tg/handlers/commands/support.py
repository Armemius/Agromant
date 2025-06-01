from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from tg.decorators.command_handler import command_handler
from tg.utils.constants import SUPPORT_KEYBOARD_BUTTON


@command_handler(name="support", aliases=[SUPPORT_KEYBOARD_BUTTON])
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.delete()

    await update.message.reply_text(
        """
🛟 Если у тебя возникли вопросы или предложения по работе бота, ты можешь обратиться в [службу поддержки](https://t.me/armemius)
        """,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
