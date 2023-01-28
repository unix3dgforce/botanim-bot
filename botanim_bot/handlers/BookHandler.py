import telegram
from telegram import Update
from telegram.ext import ContextTypes

from botanim_bot.common import Messages
from botanim_bot.common.Utils import Utils
from botanim_bot.core.services import IBookService, IConfigService
from botanim_bot.handlers import BaseHandler


class BookHandler(BaseHandler):
    def __init__(self, book_service: IBookService, config_service: IConfigService):
        self._book_service = book_service
        self._config_service = config_service

    async def all_books(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        categories_with_books = list(await self._book_service.get_all_books())
        if not update.message:
            return

        await self.send_response(
            update,
            context,
            Utils.build_category_with_books_string(categories_with_books[0]),
            Utils.get_categories_keyboard(
                current_category_index=0,
                categories_count=len(categories_with_books),
                callback_prefix=self._config_service.config.all_books_callback_pattern
            ),
        )

    async def all_books_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        if not query.data or not query.data.strip():
            return
        categories_with_books = list(await self._book_service.get_all_books())

        pattern_prefix_length = self._config_service.config.all_books_callback_pattern_length
        current_category_index = int(query.data[pattern_prefix_length:])
        await query.edit_message_text(
            text=Utils.build_category_with_books_string(
                categories_with_books[current_category_index]
            ),
            reply_markup=Utils.get_categories_keyboard(
                current_category_index=current_category_index,
                categories_count=len(categories_with_books),
                callback_prefix=self._config_service.config.all_books_callback_pattern,
            ),
            parse_mode=telegram.constants.ParseMode.HTML,
        )

    async def already(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        already_read_books = await self._book_service.get_already_read_books()
        books = []
        for index, book in enumerate(already_read_books, 1):
            books.append(Messages.ALREADY_BOOK.format(index=index, book=book))

        response = Messages.ALREADY.format(books="\n".join(books))
        await self.send_response(update, context, response)

    async def now(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        now_read_books = await self._book_service.get_now_reading_books()
        books = []
        just_one_book = len(tuple(now_read_books)) == 1
        for index, book in enumerate(now_read_books, 1):
            if not just_one_book:
                prefix = f"{index}. "
            else:
                prefix = ""
            books.append(Messages.NOW_BOOK.format(index=f"{prefix}", book=book))

        response = Messages.NOW.format(books="\n".join(books))
        await self.send_response(update, context, response)
