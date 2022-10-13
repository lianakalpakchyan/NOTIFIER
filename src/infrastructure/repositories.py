import os

from dotenv import load_dotenv
from pathlib import Path
from src.core.entities import EnvItemEntity
from src.core.exceptions import InfrastructureException
from src.core.repositories import BaseRepository


class ConfigRepo(BaseRepository):
    def __init__(self, path: Path):
        """This method will receive a base directory path of application
        where is stored a .env file"""
        load_dotenv(dotenv_path=path)

    def get_one(self, config_key):
        """This method will return a EnvItemEntity"""
        config_value = os.getenv(config_key)

        if config_value is None:
            raise InfrastructureException('Invalid .env key')

        return EnvItemEntity(config_key, config_value)

