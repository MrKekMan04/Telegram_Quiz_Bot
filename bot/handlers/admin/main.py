from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext

from bot.database import sql_helper
from bot.misc.other import create_buttons, reset_state
from bot.misc.states import States


async def __manage_quiz(message: types.Message, state: FSMContext) -> None:
    bot: Bot = message.bot
    chat_id = message.chat.id

    await state.set_state(States.managing_questions)
    await bot.send_message(chat_id,
                           "Выберите операцию",
                           reply_markup=create_buttons(
                               ["Создать новый опрос ➕",
                                "Удалить опрос ❌",
                                "Назад ⬅"]))


async def __create_new_quiz(message: types.Message, state: FSMContext) -> None:
    bot: Bot = message.bot
    chat_id = message.chat.id

    await state.set_state(States.creating_questions)
    await state.set_data(data={"questions": []})
    await bot.send_message(chat_id,
                           "Введите вопрос",
                           reply_markup=create_buttons(
                               ["Завершить создание ❌"]))


async def __remove_quiz(message: types.Message, state: FSMContext) -> None:
    bot: Bot = message.bot
    chat_id = message.chat.id

    if sql_helper.drop_table(sql_helper.QUESTIONS_TABLE_NAME):
        await bot.send_message(chat_id, "Опрос был успешно удалён!")
    else:
        await bot.send_message(chat_id, "Активных опросов нет!")
    await reset_state(bot, chat_id, state)


async def __return_back(message: types.Message, state: FSMContext):
    bot: Bot = message.bot
    chat_id = message.chat.id
    await reset_state(bot, chat_id, state)


async def __create_question(message: types.Message, state: FSMContext) -> None:
    bot: Bot = message.bot
    chat_id = message.chat.id
    text = str(message.text).lower().strip()
    questions = dict(await state.get_data()).get("questions")
    if text == "завершить создание ❌":
        if len(questions) > 0:
            sql_helper.drop_table(sql_helper.QUESTIONS_TABLE_NAME)
            sql_helper.add_questions(questions)
        else:
            await bot.send_message(chat_id,
                                   "Не было получено ни одного вопроса.\n"
                                   "В целях безопасности активным останется предыдущий опрос, если он был.")

        await reset_state(bot, chat_id, state)
        return

    questions.append((text, ""))

    await state.set_data(data={"questions": questions})
    await bot.send_message(chat_id,
                           "Введите следующий вопрос или завершите создание",
                           reply_markup=create_buttons(
                               ["Завершить создание ❌"]))


async def __reset_state(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    bot: Bot = callback_query.bot
    await reset_state(bot, callback_query.message.chat.id, state)
    await callback_query.message.delete_reply_markup()


def register_admin_handlers(dp: Dispatcher) -> None:
    # region Message handlers

    dp.register_message_handler(__manage_quiz,
                                content_types=["text"],
                                text="Управление опросами 🔏",
                                state=States.main_menu)

    dp.register_message_handler(__create_new_quiz,
                                content_types=["text"],
                                text="Создать новый опрос ➕",
                                state=States.managing_questions)

    dp.register_message_handler(__remove_quiz,
                                content_types=["text"],
                                text="Удалить опрос ❌",
                                state=States.managing_questions)

    dp.register_message_handler(__return_back,
                                content_types=["text"],
                                text="Назад ⬅",
                                state=States.managing_questions)

    dp.register_message_handler(__create_question,
                                content_types=["text"],
                                state=States.creating_questions)

    # endregion

    # region Callback handlers

    dp.register_callback_query_handler(__reset_state,
                                       lambda c: c.data == "cancel",
                                       state="*")

    # endregion
