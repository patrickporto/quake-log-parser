from quake_log_parser.parser.token import Token
from quake_log_parser.parser.token_entity import Entity

COMMAND_TOKENS = [
    "InitGame",
    "Exit",
    "ClientConnect",
    "ClientUserinfoChanged",
    "ClientBegin",
    "ClientDisconnect",
    "ShutdownGame",
    "Kill",
    "Item",
]

KEYWORDS = ["killed", "by"]

DELIMITERS = [
    ":",
    " ",
    "\n",
]


class Tokenizer:
    def tokenize(self, log_record):
        tokens = []
        for character in list(log_record):
            token = self.get_token(character)
            tokens.append(token)
        pipeline = [
            self.recognize_words,
            self.recognize_numbers,
            self.recognize_time,
            self.recognize_commands,
            self.recognize_keywords,
            self.recognize_arguments,
            self.clean_tokens,
        ]
        return self.apply_pipeline(pipeline, tokens)

    def apply_pipeline(self, pipeline, tokens):
        for method in pipeline:
            tokens = method(tokens)
        return tokens

    def get_token(self, character):
        if character.isdigit():
            return Token(entity=Entity.NUMBER, value=character)
        elif character.isalpha() or character in ["_", "<", ">", "\\"]:
            return Token(entity=Entity.WORD, value=character)
        elif character in DELIMITERS:
            return Token(entity=Entity.DELIMITER, value=character)
        return Token(entity=Entity.UNKNOWN, value=character)

    def clean_tokens(self, tokens):
        return [token for token in tokens if token.value.strip() != ""]

    def recognize_words(self, tokens):
        result = []
        last_token = None
        for token in tokens:
            if (
                token.entity == Entity.WORD
                and last_token
                and last_token.entity == Entity.WORD
            ):
                result[-1].append_value(token.value)
            else:
                result.append(token)
            last_token = token
        return result

    def recognize_numbers(self, tokens):
        result = []
        last_token = None
        for token in tokens:
            if (
                token.entity == Entity.NUMBER
                and last_token
                and last_token.entity == Entity.NUMBER
            ):
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
            if token.entity == Entity.NUMBER and last_token and last_token.value == ":":
                is_time = True
                result.pop()
                result[-1].append_value(":")
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
            if is_argument and token.entity not in [
                Entity.COMMAND,
                Entity.DELIMITER,
                Entity.KEYWORD,
            ]:
                token.entity = Entity.COMMAND_ARGUMENT
            result.append(token)
        return self.escape_arguments(result)

    def escape_arguments(self, tokens):
        result = []
        escape = False
        for token in tokens:
            if token.entity == Entity.COMMAND_ARGUMENT and token.value.startswith(
                "n\\"
            ):
                escape = True
            elif escape:
                result[-1].append_value(token.value, strip=False)
                continue
            result.append(token)
        return result
