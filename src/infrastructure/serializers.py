from typing import Dict
from src.core.entities import EventEntity


class EventSerializers:
    @staticmethod
    def serialize(event_entity: EventEntity) -> Dict:
        """This method will transform the EventEntity to a python dict"""

        dict_entity = {
            "event_type": event_entity.event_type,
            "body": event_entity.body,
            "to": event_entity.to,
        }

        return dict_entity

    @staticmethod
    def deseerialize(event_data: Dict) -> EventEntity:
        """This method will transform python dict to EventEntity """
        event_type = event_data.get('event_type')
        body = event_data.get('body')
        to = event_data.get('to')
        event_entity = EventEntity(event_type, body, to)

        return event_entity



