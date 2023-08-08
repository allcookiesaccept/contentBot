from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from db.data import REPRISE, TASKS, DESCRIPTIONLESS_SITIES, PHOTOLESS_SITES


class Keyboard:
    def __init__(self):
        self.__activate_keyboard_lists()
        self.__activate_keyboard_chat_objects()

    def __activate_keyboard_lists(self):
        self.reprise_answers = [[KeyboardButton(text=message)] for message in REPRISE]
        self.photo_acceptors = [
            [KeyboardButton(text=message)] for message in PHOTOLESS_SITES
        ]
        self.description_acceptors = [
            [KeyboardButton(text=message)] for message in DESCRIPTIONLESS_SITIES
        ]
        self.tasks = [[KeyboardButton(text=message)] for message in TASKS]

    def __activate_keyboard_chat_objects(self):
        self.REPRISE = ReplyKeyboardMarkup(
            keyboard=self.reprise_answers,
            resize_keyboard=True,
        )

        self.PHOTO_ACCEPTOR = ReplyKeyboardMarkup(
            keyboard=self.photo_acceptors,
            resize_keyboard=True,
        )

        self.DESCRIPTION_ACCEPTOR = ReplyKeyboardMarkup(
            keyboard=self.description_acceptors,
            resize_keyboard=True,
        )

        self.TASK_TYPE = ReplyKeyboardMarkup(
            keyboard=self.tasks,
            resize_keyboard=True,
        )


keys = Keyboard()
