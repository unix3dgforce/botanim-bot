import aiosqlite
from typing import Optional, Iterable, Any, LiteralString

from botanim_bot.data.db import IDatabase


class SQLiteDatabase(IDatabase):
    def __init__(self, connection_string: str):
        super().__init__(connection_string)
        self._connection: aiosqlite.Connection | None = None

    @property
    def connection(self) -> aiosqlite.Connection:
        return self._connection

    async def _get_cursor(self, sql: LiteralString, params: Optional[Iterable[Any]]) -> aiosqlite.Cursor:
        args: tuple[LiteralString, Optional[Iterable[Any]]] = (sql, params)
        cursor = await self.connection.execute(*args)
        self.connection.row_factory = aiosqlite.Row
        return cursor

    def _get_result_with_column_names(self, cursor: aiosqlite.Cursor, row: aiosqlite.Row) -> dict:
        column_names = [d[0] for d in cursor.description]
        resulting_row = {}
        for index, column_name in enumerate(column_names):
            resulting_row[column_name] = row[index]
        return resulting_row

    async def connect(self, *args, **kwargs):
        if not self.connection:
            self._connection = await aiosqlite.connect(self.connection_string)

    async def close(self, *args, **kwargs) -> None:
        if self.connection:
            await self.connection.close()

    async def fetch_one(self, sql: LiteralString, params: Optional[Iterable[Any]] = None) -> dict | None:
        cursor = await self._get_cursor(sql, params)
        if not (row_ := await cursor.fetchone()):
            return None

        return self._get_result_with_column_names(cursor, row_)

    async def fetch_all(self, sql: LiteralString, params: Optional[Iterable[Any]] = None) -> list[dict]:
        results = []
        cursor = await self._get_cursor(sql, params)
        for row_ in await cursor.fetchall():
            results.append(self._get_result_with_column_names(cursor, row_))

        return results

    async def execute(self, sql: LiteralString, params: Optional[Iterable[Any]] = None) -> None:
        args: tuple[LiteralString, Optional[Iterable[Any]]] = (sql, params)
        try:
            await self.connection.execute(*args)
            await self.connection.commit()
        except aiosqlite.Error:
            await self.connection.rollback()




