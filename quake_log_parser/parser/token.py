from dataclasses import dataclass

from quake_log_parser.parser.token_entity import Entity


@dataclass
class Token:
    entity: Entity = Entity.UNKNOWN
    value: str = ""

    def append_value(self, value, strip=True):
        new_value = self.value + value
        if strip:
            self.value = new_value.strip()
        else:
            self.value = new_value
