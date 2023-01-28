from __future__ import annotations
from datetime import datetime
from typing import Iterable

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from botanim_bot.core.models import CategoryModel


class Utils:
    @staticmethod
    def format_book_name(book_name_with_author: str) -> str:
        try:
            book_name, author = tuple(map(str.strip, book_name_with_author.split("::")))
        except ValueError:
            return book_name_with_author
        return f"{book_name}. <i>{author}</i>"

    @staticmethod
    def calculate_category_books_start_index(categories: Iterable[CategoryModel], current_category: CategoryModel) -> int | None:
        start_index = 0
        for category in categories:
            if category.id != current_category.id:
                start_index += len(tuple(category.books))
            else:
                return start_index

    @staticmethod
    def build_category_with_books_string(category: CategoryModel, start_index: int | None = None) -> str:
        response = [f"<b>{category.name}</b>\n\n"]
        for index, book in enumerate(category.books, 1):
            if start_index is None:
                prefix = "◦"
            else:
                prefix = f"{start_index + index}."
            response.append(f"{prefix} {Utils.format_book_name(book.name)}\n")
        return "".join(response)

    @staticmethod
    def books_to_words(books_count: int) -> str:
        days = ["книга", "книги", "книг"]
        if books_count % 10 == 1 and books_count % 100 != 11:
            p = 0
        elif 2 <= books_count % 10 <= 4 and (
                books_count % 100 < 10 or books_count % 100 >= 20
        ):
            p = 1
        else:
            p = 2
        return days[p]

    @staticmethod
    def get_categories_keyboard(current_category_index: int, categories_count: int, callback_prefix: str) -> InlineKeyboardMarkup:
        prev_index = current_category_index - 1
        if prev_index < 0:
            prev_index = categories_count - 1
        next_index = current_category_index + 1
        if next_index > categories_count - 1:
            next_index = 0
        keyboard = [
            [
                InlineKeyboardButton("<", callback_data=f"{callback_prefix}{prev_index}"),
                InlineKeyboardButton(
                    f"{current_category_index + 1}/{categories_count}", callback_data=" "
                ),
                InlineKeyboardButton(
                    ">",
                    callback_data=f"{callback_prefix}{next_index}",
                ),
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

