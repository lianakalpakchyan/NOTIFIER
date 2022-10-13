import os
from pathlib import Path
from dotenv import find_dotenv
from unittest import TestCase

from src.core.entities import EnvItemEntity
from src.infrastructure.repositories import ConfigRepo


class ConfigRepository(TestCase):
    def setUp(self) -> None:
        path = Path(find_dotenv())
        self.repo = ConfigRepo(path)

    def test_get_one_should_return_EnvItemEntity_slack_api_token(self):
        slack_api_token_entity = self.repo.get_one('SLACK_API_TOKEN')

        test_slack_api_token_entity = EnvItemEntity('SLACK_API_TOKEN', os.getenv('SLACK_API_TOKEN'))
        self.assertEqual(slack_api_token_entity.key, test_slack_api_token_entity.key)
        self.assertEqual(slack_api_token_entity.value, test_slack_api_token_entity.value)

    def test_get_one_should_return_EnvItemEntity_email_secret_key(self):
        email_secret_key_entity = self.repo.get_one('EMAIL_SECRET_KEY')

        test_email_secret_key_entity = EnvItemEntity('EMAIL_SECRET_KEY', os.getenv('EMAIL_SECRET_KEY'))
        self.assertEqual(email_secret_key_entity.key, test_email_secret_key_entity.key)
        self.assertEqual(email_secret_key_entity.value, test_email_secret_key_entity.value)

    def test_get_one_should_return_EnvItemEntity_email_address(self):
        email_address_entity = self.repo.get_one('EMAIL_ADDRESS')

        test_email_address_entity = EnvItemEntity('EMAIL_ADDRESS', os.getenv('EMAIL_ADDRESS'))
        self.assertEqual(email_address_entity.key, test_email_address_entity.key)
        self.assertEqual(email_address_entity.value, test_email_address_entity.value)

