import json
import os

from unittest import TestCase

from src.infrastructure.controllers import APIController


class TestAPIController(TestCase):
    program_answers = [
        'email success', 'email success', 'email fail', 'not send',
        'message success', 'not send', 'message success'
    ]

    def setUp(self) -> None:
        self.controller = APIController()
        self.controller_approved = []
        self.controller_new = []

        approved_path = os.path.join('.', 'tests', 'events', 'approved_publication.json')
        new_path = os.path.join('.', 'tests', 'events', 'new_publication.json')

        with open(approved_path) as approved, open(new_path) as new:
            approved_list = json.load(approved)
            new_list = json.load(new)

            for event in approved_list:
                self.controller_approved.append(event)

            for event in new_list:
                self.controller_approved.append(event)

    def test_process_event(self):
        for event, answer in zip(self.controller_approved, self.program_answers):
            self.assertEqual(self.controller.process_event(event), answer)

