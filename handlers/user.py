from aiogram import Router
from keyboards.keyboards import keys
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile, Update
from aiogram.filters import Command
from aiogram.filters.text import Text
from services.xml.photos import PhotoMatcher
from services.xml.descriptions import DescriptionMatcher
from config.models import CSVFile
from services.csv.worker import CSVWorker
from config.data import DESCRIPTIONLESS_SITIES, PHOTOLESS_SITES
from aiogram import Dispatcher

CHUNK_SIZE = 2000


class BotRouter(Router):
    def __init__(self, dp: Dispatcher):
        super().__init__()
        self.dp = dp
        self.init_handlers()

    def init_handlers(self):
        self.message.register(self.start_command, Command("start"))
        self.message.register(self.goodbye_message, Text(text="В другой раз."))
        self.message.register(self.one_more_time_please, Text(text="Почему бы и нет?"))
        self.message.register(self.start_photo_task, Text(text="Загрузить фотографии"))
        self.message.register(self.choose_donor_for_photos, Text(text=PHOTOLESS_SITES))
        self.message.register(self.start_description_task, Text(text="Добавить описания"))
        self.message.register(self.choose_donor_for_descriptions, Text(text=DESCRIPTIONLESS_SITES))


    async def start_command(self, message: Message):
        await message.answer("С чего начнем?", reply_markup=keys.TASK_TYPE)

    async def goodbye_message(self, message: Message):
        await message.reply("До встречи!", reply_markup=ReplyKeyboardRemove())

    async def one_more_time_please(self, message: Message):
        await message.reply("Что на этот раз?", reply_markup=keys.TASK_TYPE)

    async def start_photo_task(self, message: Message):
        await message.reply("На какой?", reply_markup=keys.PHOTO_ACCEPTOR)

    async def start_description_task(self, message: Message):
        # some_code
        await message.reply("На какой?", reply_markup=keys.DESCRIPTION_ACCEPTOR)

    async def choose_donor_for_photos(self,message: Message):
        photo_acceptor = message.text.split(": ")[-1]
        photo_matcher = PhotoMatcher()
        processed_data: CSVFile = photo_matcher(photo_acceptor)
        if processed_data == "No photos":
            await message.answer("Не нашлось подходящих фотографий")
        elif isinstance(processed_data, CSVFile):
            dataframe = CSVWorker(processed_data)
            file_path = dataframe()
            input_file = FSInputFile(file_path[0])
            await message.answer_document(input_file)

        await message.answer(f"Повторить?", reply_markup=keys.REPRISE)


    async def choose_donor_for_descriptions(self, message: Message):
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
