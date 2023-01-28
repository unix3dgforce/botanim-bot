import dataclasses


@dataclasses.dataclass
class BookVoteResultModel:
    book_name: str
    score: int
