import logging
from typing import Iterable

from botanim_bot.core.models import VotingModel, VoteResultsModel, BookModel, BookVoteResultModel
from botanim_bot.core.services import IVotingService, IUserService, IConfigService
from botanim_bot.data.db import IDatabase


logger = logging.getLogger(__name__)


class VotingService(IVotingService):
    def __init__(self, db: IDatabase, user_service: IUserService, config_service: IConfigService):
        self._db = db
        self._user_service = user_service
        self._config_service = config_service

    async def get_actual_voting(self) -> VotingModel | None:
        sql = """
                SELECT id, voting_start, voting_finish
                FROM voting
                WHERE voting_start <= current_date
                    AND voting_finish >= current_date
                ORDER BY voting_start
                LIMIT 1
            """

        voting = await self._db.fetch_one(sql)
        if not voting:
            return None

        return VotingModel(
            id=voting["id"],
            voting_start=voting["voting_start"],
            voting_finish=voting["voting_finish"],
            date_format=self._config_service.config.date_format
        )

    async def vote(self, telegram_user_id: int, books: Iterable[BookModel]) -> None:
        await self._user_service.user_add(telegram_user_id)
        actual_voting = await self.get_actual_voting()
        if actual_voting is None:
            logger.warning("No actual voting in save_vote()")
            return

        sql = """
                INSERT OR REPLACE INTO vote
                    (vote_id, user_id, first_book_id, second_book_id, third_book_id)
                VALUES (:vote_id, :user_id, :first_book, :second_book, :third_book)
                """
        books = tuple(books)
        await self._db.execute(
            sql,
            {
                "vote_id": actual_voting.id,
                "user_id": telegram_user_id,
                "first_book": books[0].id,
                "second_book": books[1].id,
                "third_book": books[2].id,
            },
        )

    async def get_leaders(self) -> VoteResultsModel | None:
        actual_voting = await self.get_actual_voting()
        if actual_voting is None:
            return None

        vote_results = VoteResultsModel(
            voting=VotingModel(
                id=actual_voting.id,
                voting_start=actual_voting.voting_start,
                voting_finish=actual_voting.voting_finish,
                date_format=self._config_service.config.date_format
            ),
            leaders=[],
        )

        sql = """
                SELECT t2.*, b.name as book_name
                FROM (SELECT t.book_id, sum(t.score) as score from (
                    SELECT first_book_id AS book_id, 3*count(*) AS score
                    FROM vote v
                    WHERE vote_id=(:voting_id)
                    GROUP BY first_book_id

                    UNION

                    SELECT second_book_id AS book_id, 2*count(*) AS score
                    FROM vote v
                    WHERE vote_id=(:voting_id)
                    GROUP BY second_book_id

                    UNION

                    SELECT third_book_id AS book_id, 1*count(*) AS score
                    FROM vote v
                    WHERE vote_id=(:voting_id)
                    GROUP BY third_book_id
                ) t
                GROUP BY book_id
                ORDER BY sum(t.score) DESC
                LIMIT 10) t2
                LEFT JOIN book b on b.id=t2.book_id
            """

        rows = await self._db.fetch_all(sql, {"voting_id": actual_voting.id})
        for row in rows:
            vote_results.leaders.append(
                BookVoteResultModel(book_name=row["book_name"], score=row["score"])
            )

        return vote_results
