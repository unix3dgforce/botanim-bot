from typing import Iterable, cast, LiteralString

from botanim_bot.core.models import BookModel, CategoryModel
from botanim_bot.core.services import IBookService, IConfigService
from botanim_bot.data.db import IDatabase


class BookService(IBookService):
    def __init__(self, db: IDatabase, config_service: IConfigService):
        self._db = db
        self._config_service = config_service

    async def get_all_books(self) -> Iterable[CategoryModel]:
        sql = f"""{self._get_books_base_sql()}
                      ORDER BY c."ordering", b."ordering" """
        books = await self._get_books_from_db(sql)
        return self._group_books_by_categories(books)

    async def get_not_started_books(self) -> Iterable[CategoryModel]:
        sql = f"""{self._get_books_base_sql()}
                      WHERE b.read_start IS NULL
                      ORDER BY c."ordering", b."ordering" """
        books = await self._get_books_from_db(sql)
        return self._group_books_by_categories(books)

    async def get_already_read_books(self) -> Iterable[BookModel]:
        sql = f"""{self._get_books_base_sql()}
                      WHERE read_start<current_date
                          AND read_finish  <= current_date
                      ORDER BY b.read_start"""
        return await self._get_books_from_db(sql)

    async def get_now_reading_books(self) -> Iterable[BookModel]:
        sql = f"""{self._get_books_base_sql()}
                      WHERE read_start<=current_date
                          AND read_finish>=current_date
                      ORDER BY b.read_start"""
        return await self._get_books_from_db(sql)

    async def get_books_by_numbers(self, numbers: Iterable[int]) -> Iterable[BookModel]:
        numbers_joined = ", ".join(map(str, map(int, numbers)))

        hardcoded_sql_values = []
        for index, number in enumerate(numbers, 1):
            hardcoded_sql_values.append(f"({number}, {index})")
        hardcoded_sql_values = ", ".join(hardcoded_sql_values)

        base_sql = self._get_books_base_sql(
            'ROW_NUMBER() over (order by c."ordering", b."ordering") as idx'
        )
        sql = f"""
                SELECT t2.* FROM (
                  VALUES {hardcoded_sql_values}
                ) t0
                INNER JOIN
                (
                SELECT t.* FROM (
                    {base_sql}
                    WHERE read_start IS NULL
                ) t
                WHERE t.idx IN ({numbers_joined})
                ) t2
                ON t0.column1 = t2.idx
                ORDER BY t0.column2
            """
        books = await self._get_books_from_db(cast(LiteralString, sql))
        return books

    def _group_books_by_categories(self, books: Iterable[BookModel]) -> Iterable[CategoryModel]:
        categories = []
        category_id = None
        for book in books:
            if category_id != book.category_id:
                categories.append(
                    CategoryModel(id=book.category_id, name=book.category_name, books=[book])
                )
                category_id = book.category_id
                continue
            categories[-1].books.append(book)
        return categories

    def _get_books_base_sql(self, select_param: LiteralString | None = None) -> LiteralString:
        return f"""
            SELECT
                b.id as book_id,
                b.name as book_name,
                c.id as category_id,
                c.name as category_name,
                {select_param + "," if select_param else ""}
                b.read_start, b.read_finish
            FROM book b
            LEFT JOIN book_category c ON c.id=b.category_id
        """

    async def _get_books_from_db(self, sql: LiteralString) -> Iterable[BookModel]:
        books_raw = await self._db.fetch_all(sql)
        return [
            BookModel(
                id=book["book_id"],
                name=book["book_name"],
                category_id=book["category_id"],
                category_name=book["category_name"],
                read_start=book["read_start"],
                read_finish=book["read_finish"],
                date_format=self._config_service.config.date_format
            )
            for book in books_raw
        ]
