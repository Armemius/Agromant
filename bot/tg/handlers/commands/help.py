from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from tg.decorators.command_handler import command_handler
from tg.utils.constants import HELP_KEYBOARD_BUTTON


with open("resources/demo.mp4", "rb") as file:
    DEMO_VIDEO = file.read()


@command_handler(name="help", aliases=[HELP_KEYBOARD_BUTTON])
async def guide(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.delete()

    await context.bot.send_chat_action(
        update.effective_user.id,
        ChatAction.UPLOAD_VIDEO,
    )
    await update.message.reply_video(
        video=DEMO_VIDEO,
        caption="""
Пожалуйста, загрузите хорошую фотографию растения или его листьев

• Чёткий фокус на повреждённых участках или характерных признаках (пятна, изменение цвета, деформация и т.д.)
• Снимок при естественном освещении, без бликов и резких теней
• При возможности — несколько ракурсов: общий вид растения и крупный план проблемных зон

Как только фото будет загружено, я определю, что это за растение, опишу возможные проблемы и предложу варианты их решения
        """
    )