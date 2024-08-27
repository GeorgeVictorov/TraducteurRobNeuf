from aiogram import F, Router
from aiogram.types import ContentType, Message

router = Router()


@router.message(F.content_type != ContentType.TEXT)
async def send_echo(message: Message):
    await message.reply(text='Didn`t get it mate, try to type text.')
