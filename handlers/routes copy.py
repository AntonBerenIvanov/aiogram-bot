from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

router = Router()

def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="О боте")],
            [KeyboardButton(text="Старт"), KeyboardButton(text="/help")]
        ],
        resize_keyboard=True
    )

    return keyboard


def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть сайт", url="https://itproger.com")],
            [InlineKeyboardButton(text="Подробнее", callback_data="info_more")]
        ]
    )

    return keyboard

@router.callback_query(lambda c: c.data == "info_more")
async def process_more_info(callback: CallbackQuery):
    await callback.message.answer("Вот более подробная информация Калбек")
    await callback.answer()

@router.message(Command("start"))
@router.message(F.text.lower() == "старт")
async def start(message: Message):
    
    await message.answer("Привет, я твой первый бот, \n *который работает!* \n Напиши /help _для помощи_ :)", parse_mode="Markdown")
    

@router.message(Command("help"))
async def help(message: Message):
    
    await message.answer(
        "Команды: \n /start - <a herf='https://yandex.ru'>запустить бот</a> \n /help - список команд \n /about - про бот",
        parse_mode="HTML",
        reply_markup=get_main_reply_keyboard())

@router.message(Command("about"))
async def about(message: Message):
    
    await message.answer(f"Этот бот - твое первое творение, {message.from_user.first_name}",
        reply_markup=get_main_inline_keyboard())

@router.message()
async def some_text(message: Message):
    
    await message.answer("Просто текст", parse_mode="Markdown")