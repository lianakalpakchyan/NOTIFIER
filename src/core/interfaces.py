from abc import (
    ABCMeta,
    abstractmethod,
)


class BaseMessengerServiceProvider(metaclass=ABCMeta):
    @abstractmethod
    def send_message(self, event_entity):
        raise NotImplementedError


class BaseEmailServiceProvider(metaclass=ABCMeta):
    @abstractmethod
    def send_email(self, event_entity):
        raise NotImplementedError


class BaseLoggerProvider(metaclass=ABCMeta):
    @abstractmethod
    def info(self, message):
        raise NotImplementedError

    @abstractmethod
    def warning(self, message):
        raise NotImplementedError

    @abstractmethod
    def error(self, message):
        raise NotImplementedError

    @abstractmethod
    def critical(self, message):
        raise NotImplementedError

