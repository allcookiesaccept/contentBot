# https://mastergroosha.github.io/aiogram-3-guide/quickstart/
from aiogram import Bot, F, Router
from aiogram.types import Message
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command

# from aiogram.dispatcher import filters
from kb import keys
from aiogram.dispatcher.filters import Text

# from aiogram.dispatcher import filters
from aiogram.dispatcher.filters import Text


router = Router()

@router.message(F.content_type == "text")

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
    donor = message.text.split(": ")[-1]
    await message.answer(f"From {donor} to {photo_acceptor}")


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


async def cmd_continue(message: types.Message):
    await message.reply("No! You are!")


dp.register_message_handler(cmd_continue, Command("You"))


@dp.message_handler(Command("test"))
async def cmd_test(message: types.Message):
    await message.answer(f"Hi, <b>sunshine</b>!", parse_mode="HTML")


async def main():
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
