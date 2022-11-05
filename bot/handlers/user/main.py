from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext

from bot.database import sql_helper
from bot.misc.other import reset_state, generate_question, keyboard_base
from bot.misc.states import States


async def __start(message: types.Message, state: FSMContext) -> None:
    bot: Bot = message.bot
    chat_id = message.chat.id
    await bot.send_message(chat_id, "<b>Добро пожаловать в Quiz Bot!</b>")
    await reset_state(bot, chat_id, state)


async def __quiz_go(message: types.Message, state: FSMContext) -> None:
    bot: Bot = message.bot
    if len((questions := sql_helper.get_questions()[1])) != 0:
        await state.set_state(States.answering_questions)
        await state.set_data(data={"question_index": 0})
        await bot.send_message(message.chat.id, "Что ж, поехали!", reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(message.chat.id, generate_question(questions, 0), reply_markup=keyboard_base)
    else:
        await bot.send_message(message.chat.id,
                               "На данный момент опросов нет. Попробуйте повторить попытку позже.")


async def __answering_questions(message: types.Message, state: FSMContext) -> None:
    bot: Bot = message.bot
    current_question_index = dict(await state.get_data()).get("question_index")
    for i in range(len((questions := sql_helper.get_questions()[1]))):
        if i == current_question_index:
            sql_helper.add_answer(message.from_user.id,
                                  message.from_user.full_name,
                                  message.text,
                                  questions[i][0])

            if str(message.from_user.id) not in sql_helper.get_answered_users(questions[i][0]):
                sql_helper.append_responsed_users(str(message.from_user.id), questions[i][0])

            if i != len(questions) - 1:
                await state.set_data(data={"question_index": i + 1})
                await bot.send_message(message.chat.id, f"Спасибо за ответ на вопрос {i + 1}!")
                await bot.send_message(message.chat.id, generate_question(questions, i + 1), reply_markup=keyboard_base)
            else:
                await bot.send_message(message.chat.id, "Спасибо за ваши ответы! =)")
                await reset_state(bot, message.chat.id, state)
            break


def register_user_handlers(dp: Dispatcher) -> None:
    # region Message handlers

    dp.register_message_handler(__start,
                                content_types=["text"],
                                commands=["start"],
                                state="*")

    dp.register_message_handler(__quiz_go,
                                content_types=["text"],
                                text="Пройти опрос ✅",
                                state=States.main_menu)

    dp.register_message_handler(__answering_questions,
                                content_types=["text"],
                                state=States.answering_questions)

    # endregion
