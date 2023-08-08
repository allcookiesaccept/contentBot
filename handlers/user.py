from aiogram import Router
from keyboards.keyboards import keys
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile, Update
from aiogram.filters import Command
from aiogram.filters.text import Text
from services.xml.photos import PhotoMatcher
from services.xml.descriptions import DescriptionMatcher
from config.models import CSVFile
from services.csv.worker import CSVWorker
from db.data import DESCRIPTIONLESS_SITIES, PHOTOLESS_SITES
from typing import Any
from aiogram.methods.send_message import SendMessage

router = Router()

#
@router.errors()
async def error_handler(exception: Exception) -> Any:
    pass



@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("С чего начнем?", reply_markup=keys.TASK_TYPE)

def _error_call():

    return 1/0
@router.message(Text(text="Вызвать ошибку"))
async def error_try(message: Message):

    _error_call()

    await message.reply("Получилось?", reply_markup=keys.REPRISE)

@router.message(Text(text="В другой раз."))
async def goodbye_message(message: Message):

    await message.reply("До встречи!", reply_markup=ReplyKeyboardRemove())


@router.message(Text(text="Почему бы и нет?"))
async def one_more_please(message: Message):

    await message.reply("Что на этот раз?", reply_markup=keys.TASK_TYPE)

@router.message(Text(text="Загрузить фотографии"))
async def init_photo_task(message: Message):
    await message.reply(
        "На какой?", reply_markup=keys.PHOTO_ACCEPTOR
    )


@router.message(Text(text=PHOTOLESS_SITES))
async def choose_donor_for_photos(message: Message):
    photo_acceptor = message.text.split(": ")[-1]
    photo_matcher = PhotoMatcher()
    processed_data: CSVFile = photo_matcher(photo_acceptor)
    if processed_data == "No photos":
        await message.answer(f"Не нашлось подходящих фотографий")
    if type(processed_data) == CSVFile:
        dataframe = CSVWorker(processed_data)
        file_path = dataframe()
        input_file = FSInputFile(file_path[0])
        await message.answer_document(input_file)

    await message.answer(f"Повторить?", reply_markup=keys.REPRISE)


@router.message(Text(text="Добавить описания"))
async def init_description_task(message: Message):
    await message.reply(
        "На какой?", reply_markup=keys.DESCRIPTION_ACCEPTOR
    )




@router.message(Text(text=DESCRIPTIONLESS_SITIES))
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
        f"Повторить?",
        reply_markup=keys.REPRISE,
    )


@router.message(Text(text=DESCRIPTIONLESS_SITIES))
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
        f"Повторить?",
        reply_markup=keys.REPRISE,
    )
