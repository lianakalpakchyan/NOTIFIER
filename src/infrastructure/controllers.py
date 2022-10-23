from abc import ABCMeta

from src.core.use_cases import NotifierUseCase
from src.infrastructure.serializers import EventSerializers
from src.infrastructure.services import (
    SlackService,
    EmailService,
    LoggerService
)
from src.infrastructure.providers import (
    SlackMessengerProvider,
    EmailServiceProvider,
    LoggerProvider
)

from src.infrastructure import config
from src.infrastructure.repositories import ConfigRepo

from dotenv import find_dotenv
from pathlib import Path

DOTENV_PATH = Path(find_dotenv())


class BaseController(metaclass=ABCMeta):
    def __init__(self):
        self._slack_service = None
        self._email_service = None
        self._logger_service = None
        self._env_repo = None
        self._email_service_provider = None
        self._messenger_service_provider = None
        self._logger_service_provider = None

    @property
    def env_repo(self):
        self._env_repo = ConfigRepo(DOTENV_PATH)
        return self._env_repo

    @property
    def logger_service(self) -> LoggerService:
        if self._logger_service is None:
            self._logger_service = LoggerService(__name__)
        return self._logger_service

    @property
    def logger_provider(self) -> LoggerProvider:
        if self._logger_service_provider is None:
            self._logger_service_provider = LoggerProvider(self.logger_service)
        return self._logger_service_provider

    @property
    def slack_service(self) -> SlackService:
        if self._slack_service is None:
            api_token = self.env_repo.get_one(config.SLACK_API_TOKEN).value
            channel = self.env_repo.get_one(config.SLACK_CHANNEL_ID).value
            self._slack_service = SlackService(self.logger_provider, api_token, channel)
        return self._slack_service

    @property
    def messanger_provider(self) -> SlackMessengerProvider:
        if self._messenger_service_provider is None:
            self._messenger_service_provider = SlackMessengerProvider(self.logger_provider, self.slack_service)
        return self._messenger_service_provider

    @property
    def email_service(self) -> EmailService:
        if self._email_service is None:
            api_key = self.env_repo.get_one(config.EMAIL_API_KEY).value
            secret_key = self.env_repo.get_one(config.EMAIL_SECRET_KEY).value
            email_address = self.env_repo.get_one(config.EMAIL_ADDRESS).value
            self._email_service = EmailService(self.logger_provider, api_key, secret_key, email_address)
        return self._email_service

    @property
    def email_provider(self) -> EmailServiceProvider:
        if self._email_service_provider is None:
            self._email_service_provider = EmailServiceProvider(self.logger_provider, self.email_service)
        return self._email_service_provider


class APIController(BaseController):
    def process_event(self, event_entity):
        """This method creates a corresponding use_case instance and executes it."""
        event_entity = EventSerializers.deseerialize(event_entity)
        use_case = NotifierUseCase(event_entity, self.email_provider, self.messanger_provider)

        return use_case.execute()



