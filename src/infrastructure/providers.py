import smtplib

import slack_sdk
import slack_sdk.errors

from src.core.interfaces import (
    BaseMessengerServiceProvider,
    BaseEmailServiceProvider,
    BaseLoggerProvider
)
from email_validator import validate_email, EmailNotValidError
from src.infrastructure import serializers
import warnings


class SlackMessengerProvider(BaseMessengerServiceProvider):
    def __init__(self, logger_provider, slack_service):
        self._logger_provider = logger_provider
        self._service = slack_service
        self._event_entity = None
        warnings.filterwarnings(action="ignore", category=ResourceWarning)

    @property
    def logger_provider(self):
        return self._logger_provider

    @property
    def service(self):
        return self._service

    @property
    def event_entity(self):
        return self._event_entity

    def send_message(self, event_entity):
        answer = 'message fail'
        self._event_entity = serializers.EventSerializers.serialize(event_entity)

        try:
            channel = self.service.channel
            text = self.event_entity.get('body')
            self.service.client.chat_postMessage(channel=channel, text=text)
            self.logger_provider.info('Message is successfully send')
            answer = 'message success'
        except slack_sdk.errors.SlackApiError as error:
            self.logger_provider.error(error)

        return answer


class EmailServiceProvider(BaseEmailServiceProvider):
    def __init__(self, logger_provider, email_service):
        self._logger_provider = logger_provider
        self._service = email_service
        self._server = smtplib.SMTP('smtp.gmail.com', 587)
        self._event_entity = None

    @property
    def logger_provider(self):
        return self._logger_provider

    @property
    def service(self):
        return self._service

    @property
    def server(self):
        return self._server

    @property
    def event_entity(self):
        return self._event_entity

    def send_email(self, event_entity):
        self._event_entity = serializers.EventSerializers.serialize(event_entity)
        answer = 'email fail'

        try:
            self.server.connect('smtp.gmail.com', 587)
            self.server.starttls()
            self.server.login(self.service.sender_email_address, self.service.secret_key)
        except smtplib.SMTPAuthenticationError as error:
            self.logger_provider.error(error)

        try:
            text = self.event_entity.get('body')
            to = self.event_entity.get('to')

            # email validation
            try:
                validation = validate_email(to, check_deliverability=True)
                to = validation.email

            except EmailNotValidError as e:
                to = None
                self.logger_provider.error(e)

            if to:
                answer = 'email success'
                self.server.sendmail(self.service.sender_email_address, to, text)
                self.logger_provider.info('Mail is successfully send')

        except smtplib.SMTPSenderRefused as error:
            self.logger_provider.error(error)
        except smtplib.SMTPDataError as error:
            self.logger_provider.error(error)
        finally:
            self.server.quit()

        return answer


class LoggerProvider(BaseLoggerProvider):
    def __init__(self, logger_service):
        self._service = logger_service

    @property
    def service(self):
        return self._service

    def info(self, message):
        self.service.logger.info(message)

    def warning(self, message):
        self.service.logger.warning(message)

    def error(self, message):
        self.service.logger.error(message)

    def critical(self, message):
        self.service.logger.critical(message)

