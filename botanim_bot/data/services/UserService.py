from botanim_bot.core.services import IUserService
from botanim_bot.data.db import IDatabase


class UserService(IUserService):
    def __init__(self, db: IDatabase):
        self._db = db

    async def user_add(self, telegram_user_id: int) -> None:
        await self._db.execute(
            "INSERT OR IGNORE INTO bot_user (telegram_id) VALUES (:telegram_id)", {"telegram_id": telegram_user_id},
        )
