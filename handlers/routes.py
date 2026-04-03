from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
import asyncio


router = Router()

subscribers = set()

async def notifier(bot: Bot):
    while True:
        if subscribers:
            for user_id in list(subscribers):
                try:
                    await bot.send_message(user_id, "Ваше стандартное сообщение")
                except Exception:
                    pass

        await asyncio.sleep(10)


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет!\n"
        "Я могу помочь с рассылкой!\n\n"
        "Команды:\n"
        "/subscribe - подписаться на уведомления\n"
        "/unsubscribe - отписка\n"
        )

@router.message(Command("subscribe"))
async def subscribe(message: Message):
    user_id = message.from_user.id

    subscribers.add(user_id)

    await message.answer("Вы подписались!")

@router.message(Command("unsubscribe"))
async def unsubscribe(message: Message):
    user_id = message.from_user.id

    subscribers.discard(user_id)

    await message.answer("Вы отписались!")

@router.message(Command("subscribers"))
async def subsribers_cmd(message: Message):
    if not subscribers:
        await message.answer("Подписчиков нет")
        return
    
    text = "Подписчики:\n"
    for uid in subscribers:
        text += f"{uid}\n"

    await message.answer(text)