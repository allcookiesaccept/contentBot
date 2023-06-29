from aiogram import Router
from keyboards.keyboards import keys
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.filters import Command
from aiogram.filters.text import Text
from services.xml_parser import PhotoFiller
import datetime
from aiogram.methods.send_document import SendDocument

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    # Выбрать тип задачи
    await message.answer("Определите тип задачи!", reply_markup=keys.KEYBOARD_TASK_TYPE)


@router.message(Text(text="Подтянуть фотографии"))
async def init_photo_task(message: Message):
    await message.reply(
        "Выберите сайт без фото?", reply_markup=keys.KEYBOARD_PHOTO_ACCEPTOR
    )


@router.message(Text(text=[f"Сайт без фото: {site}" for site in keys.SITES]))
async def choose_donor_for_photos(message: Message):
    global photo_acceptor
    photo_acceptor = message.text.split(": ")[-1]
    await message.answer("Выберите сайт c фото", reply_markup=keys.KEYBOARD_PHOTO_DONOR)


@router.message(Text(text=[f"Сайт с фото: {site}" for site in keys.SITES]))
async def processing_photos(message: Message):
    photo_donor = message.text.split(": ")[-1]
    photo_filler = PhotoFiller()
    file_name = (
        f"photos_from_{photo_donor}_to_{photo_acceptor}_{datetime.date.today()}.csv"
    )
    csv_data = photo_filler(photo_acceptor, photo_donor)

    csv_data.to_csv(
        f"content_files/{file_name}", encoding="utf-8", sep=";", index=False
    )
    input_file = FSInputFile(f"content_files/{file_name}")
    await message.answer_document(input_file)

    await message.answer(f"Спасибо за ответы", reply_markup=ReplyKeyboardRemove())


@router.message(Text(text="Подтянуть описания"))
async def init_description_task(message: Message):
    await message.reply(
        "Сайт без описания?", reply_markup=keys.KEYBOARD_DESCRIPTION_ACCEPTOR
    )


@router.message(Text(text=[f"Сайт без описания: {site}" for site in keys.SITES]))
async def choose_donor_for_descriptions(message: Message):
    global description_acceptor
    description_acceptor = message.text.split(": ")[-1]
    await message.answer(
        "Выберите сайт c фото", reply_markup=keys.KEYBOARD_DESCRIPTION_DONOR
    )


@router.message(Text(text=[f"Сайт с описанием: {site}" for site in keys.SITES]))
async def processing_descriptions(message: Message):
    donor = message.text.split(": ")[-1]
    await message.answer(
        f"From {donor} to {description_acceptor}\nСпасибо за ответы!",
        reply_markup=ReplyKeyboardRemove(),
    )
