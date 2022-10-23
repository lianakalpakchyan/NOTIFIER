import logging
import os
import ssl
import warnings
from slack_sdk import WebClient


class EmailService:
    def __init__(self, logger_provider, api_key, secret_key, sender_email_address):
        self._logger_provider = logger_provider
        self._api_key = api_key
        self._secret_key = secret_key
        self._sender_email_address = sender_email_address

    @property
    def logger_provider(self):
        return self._logger_provider

    @property
    def api_key(self):
        return self._api_key

    @property
    def secret_key(self):
        return self._secret_key

    @property
    def sender_email_address(self):
        return self._sender_email_address


class SlackService:
    def __init__(self, logger_provider, api_token, channel):
        warnings.filterwarnings(action="ignore", category=DeprecationWarning)
        self._logger_provider = logger_provider
        self._api_token = api_token
        self._channel = channel
        self.__client = WebClient(
            token=self.api_token,
            ssl=ssl.SSLContext(ssl.PROTOCOL_TLS),
        )

    @property
    def client(self):
        return self.__client

    @property
    def logger_provider(self):
        return self._logger_provider

    @property
    def api_token(self):
        return self._api_token

    @property
    def channel(self):
        return self._channel


class LoggerService:
    def __init__(self, name):
        self._abs_path = os.path.abspath('.')[:os.path.abspath('.').find('NOTIFIER') + 8]
        self._file_name = os.path.join(self._abs_path, 'src', 'logs', 'notifier.log')
        self._logger = logging.getLogger(name)
        self.formatted = '%(asctime)s::%(name)s:%(lineno)s::%(levelname)s::%(message)s'
        self.logger.propagate = False
        logging.basicConfig(level=logging.DEBUG)

        self.sh = logging.StreamHandler()
        self.fh = logging.FileHandler(filename=self.file_name)

        self.console_logging()
        self.file_logging()
        self.logger.debug('Logger is initialized!')

    def console_logging(self):
        self.sh.setFormatter(logging.Formatter(self.formatted))
        self.sh.setLevel(logging.DEBUG)
        self.logger.addHandler(self.sh)

    def file_logging(self):
        self.fh.setFormatter(logging.Formatter(self.formatted))
        self.fh.setLevel(logging.DEBUG)
        self.logger.addHandler(self.fh)

    @property
    def logger(self):
        return self._logger

    @property
    def file_name(self):
        return self._file_name

