import dataclasses

from botanim_bot.core.models.enums import DatabaseTypeEnum


@dataclasses.dataclass
class AppConfigModel:
    bot_token: str = dataclasses.field(default="")
    database_type: DatabaseTypeEnum = dataclasses.field(default=DatabaseTypeEnum.UNKNOWN)
    connection_string: str = dataclasses.field(default=None)
    date_format: str = dataclasses.field(default="%d.%m.%Y")
    vote_elements_count: int = dataclasses.field(default=1)
    all_books_callback_pattern: str = dataclasses.field(default="")
    vote_books_callback_pattern: str = dataclasses.field(default="")

    def __post_init__(self):
        if isinstance(self.database_type, str):
            try:
                self.database_type = DatabaseTypeEnum.__getitem__(self.database_type.upper())
            except KeyError:
                self.database_type = DatabaseTypeEnum.UNKNOWN

    @property
    def all_books_callback_pattern_length(self):
        return len(self.all_books_callback_pattern)

    @property
    def vote_books_callback_pattern_length(self):
        return len(self.vote_books_callback_pattern)
