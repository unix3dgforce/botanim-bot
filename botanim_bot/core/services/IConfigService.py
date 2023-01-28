import abc
from pathlib import Path

from botanim_bot.core.models import AppConfigModel
from botanim_bot.core.services import IService


class IConfigService(IService):

    @property
    @abc.abstractmethod
    def config(self) -> AppConfigModel:
        """Current configuration"""

    @abc.abstractmethod
    def load_configuration(self, path_to_config: Path) -> AppConfigModel:
        """Load configuration from config file"""
