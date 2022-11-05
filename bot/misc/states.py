from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    main_menu = State()
    answering_questions = State()
    managing_questions = State()
    creating_questions = State()
