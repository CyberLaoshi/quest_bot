from aiogram.fsm.state import StatesGroup, State

class Quest(StatesGroup):
    user_level = State()
    show_hints = State()
    level_one = State()
    location_one = State()
    location_two = State()
    location_three = State()
    location_two_one = State()
    location_two_two = State()
    location_two_three = State()
    location_three_one = State()
    location_three_two = State()
    location_three_one_one = State()
    location_three_one_two = State()
    location_three_one_one_one = State()
    location_three_one_one_two = State()
    location_three_one_one_three = State()

