import dataclasses

from botanim_bot.core.models import BookVoteResultModel, VotingModel


@dataclasses.dataclass
class VoteResultsModel:
    voting: VotingModel
    leaders: list[BookVoteResultModel]


