import os
from pathlib import Path

import yaml

from botanim_bot.core.models import AppConfigModel
from botanim_bot.core.services import IConfigService


class ConfigService(IConfigService):
    def __init__(self):
        self._configuration: AppConfigModel = AppConfigModel()

    @property
    def config(self) -> AppConfigModel:
        return self._configuration

    @config.setter
    def config(self, config: AppConfigModel) -> None:
        self._configuration = config

    def load_configuration(self, path_to_config: Path) -> AppConfigModel:
        if not path_to_config.exists():
            raise FileNotFoundError(f"{path_to_config}")

        with open(path_to_config, 'r') as stream:
            config_data = yaml.full_load(stream)

        config = AppConfigModel(
            bot_token=os.getenv("TELEGRAM_BOT_TOKEN", None),
            **config_data
        )
        self.config = config
        return config
