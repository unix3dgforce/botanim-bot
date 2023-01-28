import abc

from botanim_bot.core.services import IService


class IUserService(IService):
    @abc.abstractmethod
    async def user_add(self, telegram_user_id: int) -> None:
        """Add user"""
