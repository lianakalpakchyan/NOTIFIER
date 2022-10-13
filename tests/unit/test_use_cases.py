from unittest import TestCase
from unittest.mock import Mock, patch

from src.core.use_cases import NotifierUseCase
from src.infrastructure.controllers import APIController


class TestNotifierUseCase(TestCase):
    def setUp(self) -> None:
        self.event_entity = Mock()
        self.controller_approved = []
        self.controller_new = []

    @patch.object(APIController, 'email_provider')
    @patch.object(APIController, 'messanger_provider')
    def test_execute_email(self, mock1, mock2):
        self.event_entity.event_type = "approved_publication"
        self.controller = NotifierUseCase(self.event_entity, mock1, mock2)
        self.assertEqual(self.controller.execute(), 'email')

    @patch.object(APIController, 'email_provider')
    @patch.object(APIController, 'messanger_provider')
    def test_execute_messanger(self, mock1, mock2):
        self.event_entity.event_type = "new_publication"
        self.controller = NotifierUseCase(self.event_entity, mock1, mock2)
        self.assertEqual(self.controller.execute(), 'messanger')

    @patch.object(APIController, 'email_provider')
    @patch.object(APIController, 'messanger_provider')
    def test_execute_invalid_type(self, mock1, mock2):
        self.event_entity.event_type = None
        self.controller = NotifierUseCase(self.event_entity, mock1, mock2)
        self.assertEqual(self.controller.execute(), 'not send')
