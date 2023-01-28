import dataclasses
from datetime import datetime


@dataclasses.dataclass
class BookModel:
    id: int
    name: str
    category_id: int
    category_name: str
    read_start: datetime | None
    read_finish: datetime | None
    date_format: dataclasses.InitVar[str]

    def __post_init__(self, date_format):
        """Set up read_start and read_finish to needed string format"""
        for field in ("read_start", "read_finish"):
            value = getattr(self, field)
            if value is None:
                continue
            value = datetime.strptime(value, "%Y-%m-%d").strftime(date_format)
            setattr(self, field, value)
