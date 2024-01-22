import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from handlers import user_commands, quest_messages

from config_reader import config


async def main():
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
        quest_messages.router
    )

    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# меню бота
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command='/run',
            description='Начать квест'
        ),
        BotCommand(
            command="/start",
            description="Запуск бота"
        )
    ]
    await bot.set_my_commands(main_menu_commands)

if __name__ == "__main__":
    asyncio.run(main())