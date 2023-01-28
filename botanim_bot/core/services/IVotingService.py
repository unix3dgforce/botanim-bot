import abc
from typing import Iterable

from botanim_bot.core.models import BookModel, VotingModel, VoteResultsModel
from botanim_bot.core.services import IService


class IVotingService(IService):
    @abc.abstractmethod
    async def get_actual_voting(self) -> VotingModel | None:
        """Get actual voting"""

    @abc.abstractmethod
    async def vote(self, telegram_user_id: int, books: Iterable[BookModel]) -> None:
        """Save a user's vote"""

    @abc.abstractmethod
    async def get_leaders(self) -> VoteResultsModel | None:
        """Get the voting leaders"""
