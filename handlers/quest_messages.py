from aiogram import Router, F, html
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.states import Quest
from keyboards.builders import add_btn
from keyboards.reply import main, rmk
from typing import Any, Dict
from data.subloader import get_json, show_message
import os
from aiogram.types import FSInputFile

router = Router()

@router.message(Command("run"))
async def difficulty_level(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Quest.user_level)
    await message.answer("Выберите свой уровень:", reply_markup=main)


@router.message(Quest.user_level, F.text.casefold().in_(["начинающий", "продолжающий"]))
async def level_one(message: Message, state: FSMContext):
    if os.path.exists("pics/start.png"):
        photo = FSInputFile("pics/start.png")
    file_json = await get_json("quest_data.json")
    user_msg = message.text.lower()
    await state.update_data(show_hints=True)
    if user_msg == "продолжающий":
        await state.update_data(show_hints=False)
    data = await state.get_data()
    await state.set_state(Quest.level_one)
    msg_to_user = await show_message(file_json["level_one"]["text"], data["show_hints"], file_json["level_one"]["hint"])
    await message.answer_photo(photo, caption=msg_to_user, reply_markup=add_btn(file_json["level_one"]["options"]), parse_mode="HTML")


@router.message(Quest.user_level)
async def incorrect_level(message: Message, state: FSMContext):
    await message.answer("Нажмите кнопку!",
                         reply_markup=add_btn(["Начинающий", "Продолжающий"]))

@router.message(Quest.level_one, F.text.in_(["杀","跑", "站"]))
async def first_level(message: Message, state: FSMContext):
    await state.update_data(first_action=message.text)
    data = await state.get_data()
    file_json = await get_json("quest_data.json")
    if message.text == "跑":
        await state.set_state(Quest.location_two)
        msg_to_user = await show_message(file_json["location_two"]["text"], data["show_hints"],
                                         file_json["location_two"]["hint"])
        if os.path.exists("pics/running_mines.png"):
            photo = FSInputFile("pics/running_mines.png")
        await message.answer_photo(photo, caption=msg_to_user, reply_markup=add_btn(file_json["location_two"]["options"]), parse_mode="HTML")
    elif message.text == "杀":
        if os.path.exists("pics/attack_attempt.png"):
            photo = FSInputFile("pics/attack_attempt.png")
        msg_to_user = "Думаю напасть и убрать свидетеля. Пытаюсь подойти поближе, но на меня направляют автомат. Пытаюсь выхватить свое оружие, но в меня стреляют. Что-то теплое побежало из груди. Все темнеет. Падаю... Что-ж, довольно скорый конец."
        await message.answer_photo(photo, caption=msg_to_user)
        await show_summary(message, data)
    elif message.text == "站":
        if os.path.exists("pics/standing.png"):
            photo = FSInputFile("pics/standing.png")
        await state.set_state(Quest.location_three)
        msg_to_user = await show_message(file_json["location_three"]["text"], data["show_hints"],
                                         file_json["location_three"]["hint"])
        await message.answer_photo(photo, caption=msg_to_user, reply_markup=add_btn(file_json["location_three"]["options"]), parse_mode="HTML")
    else:
        await message.answer("Ошибка")

@router.message(Quest.level_one)
async def incorrect_level_one(message: Message, state: FSMContext):
    await message.answer("Нажмите кнопку!",
                         reply_markup=add_btn(["杀","跑", "站"]))

@router.message(Quest.location_two, F.text.in_(["三二一","一二三", "三一二"]))
async def loc_two_echo(message: Message, state: FSMContext):
    await state.update_data(second_action=message.text)
    data = await state.get_data()
    if message.text == "三二一" or message.text == "一二三":
        # await message.answer("Дверь не открывается... Вы проиграли")
        if os.path.exists("pics/hospital_lose.png"):
            photo = FSInputFile("pics/hospital_lose.png")
        await message.answer_photo(photo, caption="Дверь не открывается... Вы проиграли")
        await show_summary(message, data)
    elif message.text == "三一二":
        if os.path.exists("pics/hospital.png"):
            photo = FSInputFile("pics/hospital.png")
        await message.answer_photo(photo, caption="Пи-и-к. Щелкнул замок в двери. Я открыл дверь... \nПродолжение...")
        await show_summary(message, data, True)

@router.message(Quest.location_two)
async def loc_two_echo(message: Message, state: FSMContext):
    await message.answer("Нажмите кнопку!",
                         reply_markup=add_btn(["三二一","一二三", "三一二"]))

@router.message(Quest.location_three, F.text.in_(["试试", "跑"]))
async def loc_two_echo(message: Message, state: FSMContext):
    await state.update_data(third_action=message.text)
    data = await state.get_data()
    file_json = await get_json("quest_data.json")
    if message.text == "试试":
        await state.set_state(Quest.location_three_one)
        msg_to_user = await show_message(file_json["location_three_one"]["text"], data["show_hints"],
                                         file_json["location_three_one"]["hint"])
        await message.answer(msg_to_user, reply_markup=add_btn(file_json["location_three_one"]["options"]), parse_mode="HTML")
    elif message.text == "跑":
        await state.set_state(Quest.location_two)
        msg_to_user = await show_message(file_json["location_two"]["text"], data["show_hints"],
                                         file_json["location_two"]["hint"])
        await message.answer(msg_to_user, reply_markup=add_btn(file_json["location_two"]["options"]), parse_mode="HTML")
    else:
        message.answer("Ошибка")

@router.message(Quest.location_three, ~F.text.in_(["试试", "跑"]))
async def loc_two_echo(message: Message, state: FSMContext):
    await message.answer("Нажмите кнопку!",
                         reply_markup=add_btn(["试试", "跑"]))

@router.message(Quest.location_three_one, F.text.in_(["说","不说"]))
async def loc_two_echo(message: Message, state: FSMContext):
    await state.update_data(fourth_action=message.text)
    data = await state.get_data()
    file_json = await get_json("quest_data.json")
    if message.text == "说":
        await state.set_state(Quest.location_three_one_one)
        msg_to_user = await show_message(file_json["location_three_one_one"]["text"], data["show_hints"],
                                         file_json["location_three_one_one"]["hint"])
        await message.answer(msg_to_user, reply_markup=add_btn(file_json["location_three_one_one"]["options"]), parse_mode="HTML")
    elif "不说":
        await message.answer("Я решил молчать... Пограничник поднимает автомат и направляет на меня... Похоже, это конец.")
        await show_summary(message, data)
    else:
        await message.answer("Ошибка")

@router.message(Quest.location_three_one, ~F.text.in_(["说","不说"]))
async def loc_two_echo(message: Message, state: FSMContext):
    await message.answer("Нажмите кнопку!",
                         reply_markup=add_btn(["说","不说"]))

@router.message(Quest.location_three_one_one, F.text.in_(["人","口","三"]))
async def loc_two_echo(message: Message, state: FSMContext):
    await state.update_data(fifth_action=message.text)
    data = await state.get_data()
    if message.text == "人":
        await message.answer("Правильно... Продолжение")
        await show_summary(message, data, True)
    elif message.text == "口" or message.text == "三":
        await message.answer("Неправильно... Вы проиграли")
        await show_summary(message, data)
    else:
        await message.answer("Ошибка")

@router.message(Quest.location_three_one_one, ~F.text.in_(["人","口","三"]))
async def loc_two_echo(message: Message, state: FSMContext):
    await message.answer("Нажмите кнопку!",
                         reply_markup=add_btn(["人","口","三"]))

async def show_summary(message: Message, data: Dict[str, Any], positive: bool = False) -> None:
    txt_about_hints = "с подсказками" if data["show_hints"] else "без подсказок"
    actions = []
    for action in list(data.keys())[1:]:
        actions.append(data.get(action, ""))
    actions_info = "\n".join(actions)
    text = f"Вы играли {txt_about_hints}, и Вы"
    text += (
        f" <b>выжили</b>!"
        if positive
        else " <b>погибли</b>...Так жаль..."
    )
    text += f"\n\nВаши решения:\n{html.quote(actions_info)}\n\nПопробуйте еще /run"
    await message.answer(text=text, reply_markup=rmk, parse_mode="HTML")
