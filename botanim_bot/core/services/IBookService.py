import abc
from typing import Iterable

from botanim_bot.core.models import CategoryModel, BookModel
from botanim_bot.core.services import IService


class IBookService(IService):
    @abc.abstractmethod
    async def get_all_books(self) -> Iterable[CategoryModel]:
        """Get all books"""

    @abc.abstractmethod
    async def get_not_started_books(self) -> Iterable[CategoryModel]:
        """Get all unread books"""

    @abc.abstractmethod
    async def get_already_read_books(self) -> Iterable[BookModel]:
        """Get all the books you've read"""

    @abc.abstractmethod
    async def get_now_reading_books(self) -> Iterable[BookModel]:
        """Get the books we're reading right now"""

    @abc.abstractmethod
    async def get_books_by_numbers(self, numbers: Iterable[int]) -> Iterable[BookModel]:
        """Get books by id"""
