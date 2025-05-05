import os
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode

from app.bot.constants.xlxs import CAPTION_XLSX
from app.bot.main import bot


async def send_xlsx(*, tg_id: int, file_path: str):
    if not os.path.exists(file_path):
        await bot.send_message(tg_id, "❌ No XLSX file found. Please try again later.")
        return
    document = FSInputFile(file_path)
    try:
        await bot.send_document(
            chat_id=tg_id,
            document=document,
            caption=CAPTION_XLSX,
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as e:
        await bot.send_message(tg_id, f"❌ Error occurred: {str(e)}")
        raise Exception("Error sending file") from e
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
