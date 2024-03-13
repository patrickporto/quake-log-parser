from dataclasses import dataclass
from enum import Enum


class Entity(str, Enum):
    UNKNOWN = 'unknown'
    TIME = 'time'
    COMMAND = 'command'
    COMMAND_ARGUMENT = 'command_argument'


@dataclass
class Token:
    entity: Entity = Entity.UNKNOWN
    value: str = ''

    def append_value(self, value):
        self.value = (self.value + value).strip()


def clean_tokens(tokens):
    return [token for token in tokens if token.value != '']


COMMAND_TOKENS = [
    'InitGame',
    'Exit',
    'ClientConnect',
    'ClientUserinfoChanged',
    'ClientBegin',
    'ClientDisconnect',
    'ShutdownGame',
    'Kill',
    'Item'
]


def recognize_entities(tokens):
    for token in tokens:
        if token.value in COMMAND_TOKENS:
            token.entity = Entity.COMMAND
    return tokens


class Tokenizer:
    def tokenize(self, log_record):
        tokens = []
        log_record_token_index = 0
        token_entity = Entity.UNKNOWN
        while log_record_token_index < len(log_record):
            record_token = log_record[log_record_token_index]
            if record_token == '\n':
                log_record_token_index += 1
                continue
            previous_token = tokens[-1].value if len(tokens) > 0 else ''
            if record_token == ':' and previous_token.isdigit():
                tokens[-1].append_value(record_token)
                tokens[-1].entity = Entity.TIME
                log_record_token_index += 1
                continue
            if record_token == ' ':
                tokens.append(Token(
                    entity=token_entity
                ))
                log_record_token_index += 1
                continue
            if record_token == ':':
                token_entity = Entity.COMMAND_ARGUMENT
                tokens.append(Token(
                    entity=Entity.COMMAND_ARGUMENT,
                ))
                log_record_token_index += 1
                continue
            if len(tokens) == 0:
                tokens.append(Token(
                    value=record_token,
                    entity=token_entity,
                ))
                log_record_token_index += 1
                continue
            tokens[-1].append_value(record_token)
            log_record_token_index += 1

        cleaned_tokens = clean_tokens(tokens)
        return recognize_entities(cleaned_tokens)
