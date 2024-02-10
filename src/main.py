"""Main file"""

import asyncio
import logging
import os
import sys

import sentry_sdk
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from callback_queries_handlers import callback_query_handler
from command_handlers import command_handler_router
from config import SENTRY_DSN_BOT, TOKEN
from error_handler import error_handler_router
from message_handlers import message_handler_router


def setup_bot() -> tuple[Bot, Dispatcher]:
    """Sets up the bot and dispatcher."""
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(
        command_handler_router,
        message_handler_router,
        callback_query_handler,
        error_handler_router,
    )
    return bot, dp


def setup_logging_and_sentry() -> None:
    """Sets up logging and Sentry."""
    sentry_sdk.init(
        dsn=SENTRY_DSN_BOT,
        environment=os.getenv("ENVIRONMENT", "development"),
        traces_sample_rate=0.0001,
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )


async def main() -> None:
    """Main function."""
    setup_logging_and_sentry()
    bot, dp = setup_bot()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
