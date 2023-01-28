import logging
from pathlib import Path

from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from botanim_bot.core.models.enums import DatabaseTypeEnum
from botanim_bot.core.services import IConfigService
from botanim_bot.data.db import SQLiteDatabase, IDatabase
from botanim_bot.data.services import BookService, UserService, VotingService
from botanim_bot.handlers import CommonHandler, BookHandler, VoteHandler
from botanim_bot.services import ConfigService

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def create_handlers(database: IDatabase, config_service: IConfigService):
    """Dependency linker"""
    common_handler = CommonHandler()
    book_service = BookService(db=database, config_service=config_service)
    user_service = UserService(db=database)
    voting_service = VotingService(db=database, user_service=user_service, config_service=config_service)
    book_handler = BookHandler(book_service=book_service, config_service=config_service)
    vote_handler = VoteHandler(voting_service=voting_service, book_service=book_service, config_service=config_service)
    return common_handler, book_handler, vote_handler


def get_database(config_service: IConfigService) -> IDatabase:
    match config_service.config.database_type:
        case DatabaseTypeEnum.SQLITE:
            if not (connection_string := Path(__file__).resolve().parent / config_service.config.connection_string).exists():
                raise FileNotFoundError(connection_string)

            return SQLiteDatabase(connection_string=connection_string.__str__())
        case _:
            raise NotImplementedError(f"{config_service.config.database_type}")


def main():
    """Composition root"""
    config_service: IConfigService = ConfigService()
    config_service.load_configuration(Path(__file__).resolve().parent / "config.yaml")

    if not config_service.config.bot_token:
        exit("Specify TELEGRAM_BOT_TOKEN env variable")

    common_handler, book_handler, vote_handler = create_handlers(database := get_database(config_service), config_service)
    application = ApplicationBuilder()\
        .token(config_service.config.bot_token)\
        .post_init(database.connect)\
        .post_shutdown(database.close)\
        .build()

    application.add_handler(CommandHandler("start", common_handler.start))
    application.add_handler(CommandHandler("help", common_handler.help_))

    application.add_handler(CommandHandler("allbooks", book_handler.all_books))

    application.add_handler(
        CallbackQueryHandler(
            book_handler.all_books_button,
            pattern=rf"^{config_service.config.all_books_callback_pattern}(\d+)$",
        )
    )

    application.add_handler(CommandHandler("already", book_handler.already))

    application.add_handler(CommandHandler("now", book_handler.now))

    application.add_handler(CommandHandler("vote", vote_handler.vote))

    application.add_handler(
        CallbackQueryHandler(
            vote_handler.vote_button,
            pattern=rf"^{config_service.config.vote_books_callback_pattern}(\d+)$",
        )
    )
    application.add_handler(
        MessageHandler(
            filters.TEXT & (~filters.COMMAND),
            vote_handler.vote_process,
        )
    )

    application.add_handler(CommandHandler("voteresults", vote_handler.vote_results))

    application.run_polling(close_loop=True)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())

