from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardRemove
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Начинающий"),
            KeyboardButton(text="Продолжающий")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Нажмите на кнопку. Для начинающих будут подсказки",
    selective=True
)

# spec = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="Отправить гео", request_location=True),
#             KeyboardButton(text="Отправить контакт", request_contact=True),
#             KeyboardButton(text="Создать викторину", request_poll=KeyboardButtonPollType())
#         ],
#         [
#             KeyboardButton(text="НАЗАД")
#         ]
#     ],
#     resize_keyboard=True
# )

rmk = ReplyKeyboardRemove()