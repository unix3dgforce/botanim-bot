from __future__ import annotations

import abc
from typing import Self, LiteralString, Optional, Iterable, Any, TypeVar

T = TypeVar('T')


class IDatabase(metaclass=abc.ABCMeta):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    @abc.abstractmethod
    async def close(self) -> None:
        ...

    @abc.abstractmethod
    async def fetch_one(self, sql: LiteralString, params: Optional[Iterable[Any]] = None) -> dict | None:
        ...

    @abc.abstractmethod
    async def fetch_all(self, sql: LiteralString, params: Optional[Iterable[Any]] = None) -> list[dict]:
        ...

    @abc.abstractmethod
    async def execute(self, sql: LiteralString, params: Optional[Iterable[Any]] = None) -> None:
        ...

    @abc.abstractmethod
    async def connect(self):
        ...

    @property
    @abc.abstractmethod
    def connection(self) -> T:
        ...
