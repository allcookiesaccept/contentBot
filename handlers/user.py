from aiogram import Router
from keyboards.keyboards import keys
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.filters import Command
from aiogram.filters.text import Text
from services.xml.photos import PhotoMatcher
from services.xml.descriptions import DescriptionMatcher
from services.csv import CSVWorker, CSVFile


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Что надо сделать?", reply_markup=keys.KEYBOARD_TASK_TYPE)


@router.message(Text(text="Загрузить фотографии"))
async def init_photo_task(message: Message):
    await message.reply(
        "Выберите сайт без фото?", reply_markup=keys.KEYBOARD_PHOTO_ACCEPTOR
    )


@router.message(Text(text=[f"Сайт без фото: {site}" for site in keys.SITES]))
async def choose_donor_for_photos(message: Message):
    photo_acceptor = message.text.split(": ")[-1]
    photo_matcher = PhotoMatcher()
    processed_data: CSVFile = photo_matcher(photo_acceptor)
    if processed_data == "No photos":
        await message.answer(f"Не нашлось подходящих фотографий")
    else:
        dataframe = CSVWorker(processed_data)
        file_path = dataframe()
        input_file = FSInputFile(file_path[0])
        await message.answer_document(input_file)

    await message.answer(f"Спасибо за ответы", reply_markup=ReplyKeyboardRemove())


@router.message(Text(text="Добавить описания"))
async def init_description_task(message: Message):
    await message.reply(
        "Сайт без описания?", reply_markup=keys.KEYBOARD_DESCRIPTION_ACCEPTOR
    )


@router.message(Text(text=[f"Сайт без описаний: {site}" for site in keys.SITES]))
async def choose_donor_for_descriptions(message: Message):
    description_acceptor = message.text.split(": ")[-1]
    description_matcher = DescriptionMatcher()
    processed_data: CSVFile = description_matcher(description_acceptor)

    if processed_data == "No descriptions":
        await message.answer(f"Не нашлось подходящих описаний")
    else:
        descriptions = CSVWorker(processed_data)
        paths_list = descriptions()

        for path in paths_list:
            input_file = FSInputFile(path)
            await message.answer_document(input_file)

    await message.answer(
        f"Спасибо за ответы!",
        reply_markup=ReplyKeyboardRemove(),
    )
