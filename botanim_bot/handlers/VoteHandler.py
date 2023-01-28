import re
from typing import cast

import telegram
from telegram import Update, User
from telegram.ext import ContextTypes

from botanim_bot.common import Messages
from botanim_bot.common.Utils import Utils
from botanim_bot.core.services import IVotingService, IBookService, IConfigService
from botanim_bot.handlers import BaseHandler


class VoteHandler(BaseHandler):
    def __init__(self, voting_service: IVotingService, book_service: IBookService, config_service: IConfigService):
        self._voting_service = voting_service
        self._book_service = book_service
        self._config_service = config_service

    async def vote_process(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if await self._voting_service.get_actual_voting() is None:
            await self.send_response(update, context, Messages.NO_ACTUAL_VOTING)
            return

        user_message = update.message.text
        numbers = re.findall(r"\d+", user_message)
        if len(tuple(set(map(int, numbers)))) != self._config_service.config.vote_elements_count:
            await self.send_response(update, context, Messages.VOTE_PROCESS_INCORRECT_INPUT)
            return

        books = tuple(await self._book_service.get_books_by_numbers(numbers))
        if len(books) != self._config_service.config.vote_elements_count:
            await self.send_response(update, context, Messages.VOTE_PROCESS_INCORRECT_BOOKS)
            return

        await self._voting_service.vote(cast(User, update.effective_user).id, books)

    async def vote_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        if not query.data or not query.data.strip():
            return
        categories_with_books = list(await self._book_service.get_not_started_books())

        pattern_prefix_length = self._config_service.config.vote_books_callback_pattern_length
        current_category_index = int(query.data[pattern_prefix_length:])
        current_category = categories_with_books[current_category_index]

        category_books_start_index = Utils.calculate_category_books_start_index(
            categories_with_books, current_category
        )

        await query.edit_message_text(
            text=Utils.build_category_with_books_string(
                current_category, category_books_start_index
            ),
            reply_markup=Utils.get_categories_keyboard(
                current_category_index,
                len(categories_with_books),
                self._config_service.config.vote_books_callback_pattern
            ),
            parse_mode=telegram.constants.ParseMode.HTML,
        )

    async def vote(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message:
            return

        if await self._voting_service.get_actual_voting() is None:
            await self.send_response(update, context, Messages.NO_ACTUAL_VOTING)
            return

        categories_with_books = tuple(await self._book_service.get_not_started_books())
        current_category = categories_with_books[0]

        category_books_start_index = Utils.calculate_category_books_start_index(
            categories_with_books, current_category
        )

        await update.message.reply_text(
            Utils.build_category_with_books_string(current_category, category_books_start_index),
            reply_markup=Utils.get_categories_keyboard(
                0,
                len(categories_with_books),
                self._config_service.config.vote_books_callback_pattern
            ),
            parse_mode=telegram.constants.ParseMode.HTML,
        )

    async def vote_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        leaders = await self._voting_service.get_leaders()
        if leaders is None:
            await self.send_response(update, context, Messages.NO_VOTE_RESULTS)
            return

        books = []
        for index, book in enumerate(leaders.leaders, 1):
            books.append(
                Messages.VOTE_RESULT_BOOK.format(
                    index=index,
                    book_name=Utils.format_book_name(book.book_name),
                    book_score=book.score,
                )
            )
        response = Messages.VOTE_RESULTS.format(
            books="\n".join(books),
            voting_start=leaders.voting.voting_start,
            voting_finish=leaders.voting.voting_finish,
        )
        await self.send_response(update, context, response)
