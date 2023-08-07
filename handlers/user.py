from aiogram import Router
from keyboards.keyboards import keys
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.filters import Command
from aiogram.filters.text import Text
from services.xml.photos import PhotoMatcher
from services.xml.descriptions import DescriptionFiller
from services.csv import CSVWorker, CSVFile


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Определите тип задачи!", reply_markup=keys.KEYBOARD_TASK_TYPE)


@router.message(Text(text="Подтянуть фотографии"))
async def init_photo_task(message: Message):
    await message.reply(
        "Выберите сайт без фото?", reply_markup=keys.KEYBOARD_PHOTO_ACCEPTOR
    )


@router.message(Text(text=[f"Сайт без фото: {site}" for site in keys.SITES]))
async def choose_donor_for_photos(message: Message):

    photo_acceptor = message.text.split(": ")[-1]
    photo_matcher = PhotoMatcher()
    processed_data: CSVFile = photo_matcher(photo_acceptor)
    dataframe = CSVWorker(processed_data)
    file_path = dataframe()
    input_file = FSInputFile(file_path[0])

    await message.answer_document(input_file)
    await message.answer(f"Спасибо за ответы", reply_markup=ReplyKeyboardRemove())


@router.message(Text(text="Подтянуть описания"))
async def init_description_task(message: Message):
    await message.reply(
        "Сайт без описания?", reply_markup=keys.KEYBOARD_DESCRIPTION_ACCEPTOR
    )


@router.message(Text(text=[f"Сайт без описаний: {site}" for site in keys.SITES]))
async def choose_donor_for_descriptions(message: Message):
    global description_acceptor
    description_acceptor = message.text.split(": ")[-1]
    await message.answer(
        "Сайт с описаниями", reply_markup=keys.KEYBOARD_DESCRIPTION_DONOR
    )


@router.message(Text(text=[f"Сайт с описаниями: {site}" for site in keys.SITES]))
async def processing_descriptions(message: Message):
    donor = message.text.split(": ")[-1]
    descriptions_searcher = DescriptionFiller()
    filename, df, frame_type = descriptions_searcher(description_acceptor, donor)
    descriptions = CSVWorker(filename, df, frame_type)
    paths_list = descriptions()

    for path in paths_list:
        input_file = FSInputFile(path)
        await message.answer_document(input_file)

    await message.answer(
        f"Спасибо за ответы!",
        reply_markup=ReplyKeyboardRemove(),
    )
