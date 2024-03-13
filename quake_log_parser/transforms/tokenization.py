from dataclasses import dataclass
from enum import Enum


class Entity(str, Enum):
    UNKNOWN = 'unknown'
    WORD = 'word'
    DELIMITER = 'delimiter'
    NUMBER = 'number'
    TIME = 'time'
    COMMAND = 'command'
    COMMAND_ARGUMENT = 'command_argument'
    KEYWORD = 'keyword'


@dataclass
class Token:
    entity: Entity = Entity.UNKNOWN
    value: str = ''

    def append_value(self, value):
        self.value = (self.value + value).strip()


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

KEYWORDS = [
    'killed',
    'by'
]

DELIMITERS = [
    ':',
    ' ',
    '\n',
]



class Tokenizer:
    def tokenize(self, log_record):
        tokens = []
        for character in list(log_record):
            token = self.get_token(character)
            tokens.append(token)
        tokens = self.recognize_words(tokens)
        tokens = self.recognize_numbers(tokens)
        tokens = self.recognize_time(tokens)
        tokens = self.recognize_commands(tokens)
        tokens = self.recognize_keywords(tokens)
        tokens = self.recognize_arguments(tokens)
        return self.clean_tokens(tokens)

    def get_token(self, character):
        if character.isdigit():
            return Token(entity=Entity.NUMBER, value=character)
        elif character.isalpha() or character in ['_', '<', '>']:
            return Token(entity=Entity.WORD, value=character)
        elif character in DELIMITERS:
            return Token(entity=Entity.DELIMITER, value=character)
        return Token(entity=Entity.UNKNOWN, value=character)

    def clean_tokens(self, tokens):
        return [token for token in tokens if token.value.strip() != '']

    def recognize_words(self, tokens):
        result = []
        last_token = None
        for token in tokens:
            if token.entity == Entity.WORD and last_token and last_token.entity == Entity.WORD:
                result[-1].append_value(token.value)
            else:
                result.append(token)
            last_token = token
        return result

    def recognize_numbers(self, tokens):
        result = []
        last_token = None
        for token in tokens:
            if token.entity == Entity.NUMBER and last_token and last_token.entity == Entity.NUMBER:
                result[-1].append_value(token.value)
            else:
                result.append(token)
            last_token = token
        return result

    def recognize_time(self, tokens):
        result = []
        last_token = None
        is_time = False
        for token in tokens:
            if token.entity == Entity.NUMBER and last_token and last_token.value == ':':
                is_time = True
                result.pop()
                result[-1].append_value(':')
                result[-1].entity = Entity.TIME
            if token.entity == Entity.NUMBER and is_time:
                result[-1].append_value(token.value)
            else:
                is_time = False
                result.append(token)
            last_token = token
        return result

    def recognize_commands(self, tokens):
        for token in tokens:
            if token.value in COMMAND_TOKENS:
                token.entity = Entity.COMMAND
        return tokens

    def recognize_keywords(self, tokens):
        for token in tokens:
            if token.value in KEYWORDS:
                token.entity = Entity.KEYWORD
        return tokens

    def recognize_arguments(self, tokens):
        result = []
        is_argument = False
        for token in tokens:
            if token.entity == Entity.COMMAND:
                is_argument = True
            if is_argument and token.entity not in [Entity.COMMAND, Entity.DELIMITER, Entity.KEYWORD]:
                token.entity = Entity.COMMAND_ARGUMENT
            result.append(token)
        return result
