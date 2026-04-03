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

router = Router()

@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer("Заполните анкету! \n Введите ваше имя: ")
    await state.set_state(Form.name)

@router.message(Command("cancel"))
async def cancel_form(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Анкета отклонена!")

@router.message(Form.name, F.text)
async def proccess_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer("Хорошо!\nВведите свой возраст: ")
    await state.set_state(Form.age)

@router.message(Form.age, F.text)
async def proccess_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число")
        return
    
    if int(message.text) < 1 or int(message.text) > 100:
        await message.answer("Возраст должен быть от 1 до 100")

    await state.update_data(age=int(message.text))

    await message.answer("Хорошо!\nВведите свой email: ")
    await state.set_state(Form.email)

@router.message(Form.email, F.text)
async def proccess_age(message: Message, state: FSMContext):
    email_text = message.text
    if "@" not in email_text or "." not in email_text:
        await message.answer("email не корректный")
        return
    
    await state.update_data(email=message.text)

    data = await state.get_data()
    name = data["name"]
    age = data["age"]
    email = data["email"]

    await message.answer(f"Анкета заполнена!\nИмя: {name}\nВозраст: {age}\nПочта: {email} ")
    await state.clear()

@router.message(F.photo)
async def proccess_phot(message: Message):
    photo = message.photo[-1]
    file_id = photo.file_id

    await message.answer(
        f"Вы отправили фото!\nID photo: <code>{file_id}</code>",
        parse_mode="HTML"
    )

    await message.answer_photo(file_id, caption="Вот ваше фото")


@router.message(F.video)
async def proccess_video(message: Message, bot: Bot):
    video = message.video
    file_id = video.file_id

    file = await bot.get_file(file_id)
    file_path = file.file_path

    local_path = f'downloads/{video.file_name}'

    await bot.download_file(file_path=file_path, destination=local_path)

    await message.answer("Файл сохранен!")

@router.message(Command("file"))
async def send_file(message: Message):
    file = FSInputFile('file/example.txt')

    await message.answer_document(file)