from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.misc import TgKeys
from bot.handlers import register_all_handlers


async def __on_start_up(dp: Dispatcher) -> None:
    print("Bot started successfully:\n"
          f"Id: {dp.bot.id}\n"
          f"Proxy: {dp.bot.proxy}")
    register_all_handlers(dp)


def start_bot() -> None:
    bot = Bot(token=TgKeys.TOKEN, parse_mode="HTML")
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
