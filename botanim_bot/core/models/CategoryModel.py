import dataclasses
from typing import Iterable

from botanim_bot.core.models import BookModel


@dataclasses.dataclass
class CategoryModel:
    id: int
    name: str
    books: Iterable[BookModel]
