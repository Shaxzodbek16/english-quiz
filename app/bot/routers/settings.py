from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "settings")
async def settings_command(callback: CallbackQuery) -> None:
    from_callback = callback.message
    if from_callback is None:
        return
    await from_callback.reply(
        "There is no function in Settings yet!!!:", reply_markup=None
    )
