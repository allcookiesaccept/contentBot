from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


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
        "Загрузить фотографии",
        "Добавить описания",
    ]

    def __init__(self):
        self.photo_acceptors = [
            [KeyboardButton(text=f"Сайт без фото: {site}")] for site in Keyboard.SITES
        ]
        self.photo_donors = [
            [KeyboardButton(text=f"Сайт с фото: {site}")] for site in Keyboard.SITES
        ]
        self.description_acceptors = [
            [KeyboardButton(text=f"Сайт без описаний: {site}")]
            for site in Keyboard.SITES
        ]
        self.description_donors = [
            [KeyboardButton(text=f"Сайт с описаниями: {site}")]
            for site in Keyboard.SITES
        ]
        self.tasks = [[KeyboardButton(text=f"{task}")] for task in Keyboard.TASKS]

        self.KEYBOARD_PHOTO_ACCEPTOR = ReplyKeyboardMarkup(
            keyboard=self.photo_acceptors,
            resize_keyboard=True,
        )
        self.KEYBOARD_PHOTO_DONOR = ReplyKeyboardMarkup(
            keyboard=self.photo_donors,
            resize_keyboard=True,
        )
        self.KEYBOARD_DESCRIPTION_ACCEPTOR = ReplyKeyboardMarkup(
            keyboard=self.description_acceptors,
            resize_keyboard=True,
        )
        self.KEYBOARD_DESCRIPTION_DONOR = ReplyKeyboardMarkup(
            keyboard=self.description_donors,
            resize_keyboard=True,
        )
        self.KEYBOARD_TASK_TYPE = ReplyKeyboardMarkup(
            keyboard=self.tasks,
            resize_keyboard=True,
        )


keys = Keyboard()
