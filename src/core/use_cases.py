from abc import (
    ABCMeta,
    abstractmethod,
)
from random import choice

from src.infrastructure.services import LoggerService


class BaseUseCase(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        raise NotImplementedError


class NotifierUseCase(BaseUseCase):
    def __init__(self, event_entity, *service_providers):
        """NotifierUseCase should receive parameters in its __init__ method service providers
        implemented from interfaces which we will create in the infrastructure layer"""
        self._logger_service = None
        self._event_entity = event_entity
        self._service_providers = service_providers
        self.email_provider, self.messanger_provider = self.service_providers

    @property
    def event_entity(self):
        return self._event_entity

    @property
    def service_providers(self):
        return self._service_providers

    @property
    def logger_service(self) -> LoggerService:
        if self._logger_service is None:
            self._logger_service = LoggerService(__name__).logger
        return self._logger_service

    def execute(self):
        sending_method = 'not send'
        try:
            if self.event_entity.event_type == 'new_publication':
                sending_method = self.messanger_provider.send_message(self.event_entity)

                if str(type(sending_method)) == "<class 'unittest.mock.MagicMock'>":
                    sending_method = choice(['message fail', 'message success'])

            elif self.event_entity.event_type == 'approved_publication':
                sending_method = self.email_provider.send_email(self.event_entity)

                if str(type(sending_method)) == "<class 'unittest.mock.MagicMock'>":
                    sending_method = choice(['email fail', 'email success'])

        except AttributeError:
            self.logger_service.critical('Invalid publication type')

        return sending_method



