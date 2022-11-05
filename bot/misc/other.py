from aiogram import types

from bot.misc.states import States

keyboard_base = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(
    text="Прервать опрос",
    callback_data="cancel"))


async def reset_state(bot, chat_id, state):
    keyboard = create_buttons(
        ["Пройти опрос ✅",
         "Управление опросами 🔏"])
    await state.set_state(States.main_menu)
    await bot.send_message(chat_id, "Что хотите сделать?", reply_markup=keyboard)


def generate_question(questions, index):
    return f"<b>Вопрос #{index + 1}/{len(questions)}</b>\n{questions[index][0]}"


def create_buttons(buttons, width=1):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=width)
    keyboard.add(*buttons)
    return keyboard
