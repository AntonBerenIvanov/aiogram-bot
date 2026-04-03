from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from forms.user import Form
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
import aiohttp

router = Router()

async def get_product(product_id):
    url = f"https://jsonplaceholder.typicode.com/posts/{product_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 404:
                return None
            
            data = await resp.json()
            return data

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! Я бот-магазин.\nВведите команду: /product ID\n\nПример: <b>/product 1</b>",
        parse_mode="HTML"
    )
    
@router.message(Command("product"))
async def get_product_cmd(message: Message):
    parts = message.text.strip().split()

    if len(parts) != 2:
        await message.answer("Используйте: /product 1")
        return
    
    product_id = parts[1]
    if not product_id.isdigit():
        await message.answer("ID товара должно быть числом")
        return

    await message.answer(f'Ищу товар с id: {product_id}')

    try:
        product = await get_product(int(product_id))
    except Exception:
        await message.answer('Не удалось обратиться к серверу')
        return
    
    if product is None:
        await message.answer('Такого товара не существует')
        return
    
    user_id = product.get("userId", "Нет id")
    id = product.get("id")
    title = product.get("title", "No title")
    body = product.get("body", "No body")

    text = (
        f"<b>{title}</b>\n\n"
        f"Пользователь: <i>{user_id}</i>\n"
        f"Описание: {body}"
    )

    await message.answer(text, parse_mode="HTML")