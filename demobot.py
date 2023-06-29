import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config.config import Config, load_config
from keyboards.keyboards import keys
from aiogram.filters import Text
from services.xml_parser import PhotoFiller
from pathlib import Path
import datetime


logging.basicConfig(level=logging.INFO)
config: Config = load_config()
bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
dp: Dispatcher = Dispatcher(bot=bot)
keyboard = keys()
base_dir = Path(__file__).resolve().parent


@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    # Выбрать тип задачи
    await message.answer("Определите тип задачи!", reply_markup=keys.KEYBOARD_TASK_TYPE)


@dp.message_handler(Text(equals="Подтянуть фотографии"))
async def init_photo_task(message: types.Message):
    await message.reply("Сайт без фото?", reply_markup=keys.KEYBOARD_PHOTO_ACCEPTOR)


@dp.message_handler(Text(equals=[f"Сайт без фото: {site}" for site in keys.SITES]))
async def choose_donor_for_photos(message: types.Message):
    global photo_acceptor
    photo_acceptor = message.text.split(": ")[-1]
    await message.answer("Выберите сайт c фото", reply_markup=keys.KEYBOARD_PHOTO_DONOR)


@dp.message_handler(Text(equals=[f"Сайт с фото: {site}" for site in keys.SITES]))
async def processing_photos(message: types.Message):
    photo_donor = message.text.split(": ")[-1]
    photo_filler = PhotoFiller()
    file_name = (
        f"photos_from_{photo_donor}_to_{photo_acceptor}_{datetime.date.today()}.csv"
    )
    csv_data = photo_filler(photo_acceptor, photo_donor)
    csv_data.to_csv(
        f"{base_dir}/content_files/{file_name}", encoding="utf-8", sep=";", index=False
    )

    with open(f"{base_dir}/content_files/{file_name}", "r") as file:
        await bot.send_document(message.chat.id, types.InputFile(file))

    await message.answer(f"Спасибо за ответы", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text(equals="Подтянуть описания"))
async def init_description_task(message: types.Message):
    await message.reply(
        "Сайт без описания?", reply_markup=keys.KEYBOARD_DESCRIPTION_ACCEPTOR
    )


@dp.message_handler(Text(equals=[f"Сайт без описания: {site}" for site in keys.SITES]))
async def choose_donor_for_descriptions(message: types.Message):
    global description_acceptor
    description_acceptor = message.text.split(": ")[-1]
    await message.answer(
        "Выберите сайт c фото", reply_markup=keys.KEYBOARD_DESCRIPTION_DONOR
    )


@dp.message_handler(Text(equals=[f"Сайт с описанием: {site}" for site in keys.SITES]))
async def processing_descriptions(message: types.Message):
    donor = message.text.split(": ")[-1]
    await message.answer(f"From {donor} to {description_acceptor}\nСпасибо за ответы!")


async def main():
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
