import dataclasses
from datetime import datetime


@dataclasses.dataclass
class VotingModel:
    id: int
    voting_start: str
    voting_finish: str
    date_format: dataclasses.InitVar[str]

    def __post_init__(self, date_format):
        """Set up voting_start and voting_finish to needed string format"""
        for field in ("voting_start", "voting_finish"):
            value = getattr(self, field)
            if value is None:
                continue
            try:
                value = datetime.strptime(value, "%Y-%m-%d").strftime(date_format)
            except ValueError:
                continue
            setattr(self, field, value)
