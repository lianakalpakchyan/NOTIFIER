from typing import Dict
from src.core.entities import EventEntity


class EventSerializers:
    @staticmethod
    def serialize(event_entity: EventEntity) -> Dict:
        """This method will transform the EventEntity to a python dict"""

        dict_entity: dict = dict()

        match event_entity.event_type:
            case 'new_publication':
                dict_entity = {
                    "event_type": event_entity.event_type,
                    "body": {
                        "channel": event_entity.body.get('channel'),
                        "text": event_entity.body.get('text')
                    }
                }
            case 'approved_publication':
                dict_entity = {
                    "event_type": event_entity.event_type,
                    "body": event_entity.body,
                    "to": event_entity.to,
                }

        return dict_entity

    @staticmethod
    def deseerialize(event_data: Dict) -> EventEntity:
        """his method will transform python dict to EventEntity """

        event_entity = None

        match event_data.get('event_type'):
            case 'new_publication':
                event_type = event_data.get('event_type')
                body = {
                    "channel": event_data.get('body').get('channel'),
                    "text": event_data.get('body').get('text'),
                }
                event_entity = EventEntity(event_type, body)
            case 'approved_publication':
                event_type = event_data.get('event_type')
                body = event_data.get('body')
                to = event_data.get('to')
                event_entity = EventEntity(event_type, body, to)

        return event_entity



