from aiogram import types


class Keyboard:
    SITES = [
        "iport",
        "nbcomputers",
        "nbcomgroup",
        "samsungstore",
        "s-centres",
        "micenter",
    ]

    TASKS = [
        "Подтянуть фотографии",
        "Подтянуть описания",
    ]

    def __init__(self):
        self.KEYBOARD_PHOTO_ACCEPTOR = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        )
        self.KEYBOARD_PHOTO_DONOR = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        )
        self.KEYBOARD_DESCRIPTION_ACCEPTOR = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        )
        self.KEYBOARD_DESCRIPTION_DONOR = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        )
        self.KEYBOARD_TASK_TYPE = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        )

    def __call__(self):
        for site in Keyboard.SITES:
            self.KEYBOARD_PHOTO_ACCEPTOR.add(f"Сайт без фото: {site}")
            self.KEYBOARD_PHOTO_DONOR.add(f"Сайт с фото: {site}")
            self.KEYBOARD_DESCRIPTION_ACCEPTOR.add(f"Сайт без описания: {site}")
            self.KEYBOARD_DESCRIPTION_DONOR.add(f"Сайт с описанием: {site}")

        for task in Keyboard.TASKS:
            self.KEYBOARD_TASK_TYPE.add(task)


keys = Keyboard()
