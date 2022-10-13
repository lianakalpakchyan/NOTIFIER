from abc import (
    ABCMeta,
    abstractmethod,
)


class BaseRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_one(self, token):
        raise NotImplementedError
