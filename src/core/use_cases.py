from abc import (
    ABCMeta,
    abstractmethod,
)


class BaseUseCase(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        raise NotImplementedError


class NotifierUseCase(BaseUseCase):
    def __init__(self, event_entity, *service_providers):
        """NotifierUseCase should receive parameters in its __init__ method service providers
        implemented from interfaces which we will create in the infrastructure layer"""
        self._event_entity = event_entity
        self._service_providers = service_providers
        self.email_provider, self.messanger_provider = self.service_providers

    @property
    def event_entity(self):
        return self._event_entity

    @property
    def service_providers(self):
        return self._service_providers

    def execute(self):
        sending_method = 'not send'
        try:
            match self.event_entity.event_type:
                case 'new_publication':
                    self.messanger_provider.send_message(self.event_entity)
                    sending_method = 'messanger'
                case 'approved_publication':
                    self.email_provider.send_email(self.event_entity)
                    sending_method = 'email'
        except AttributeError:
            self.email_provider.logger_provider.critical('Invalid publication type')

        return sending_method



