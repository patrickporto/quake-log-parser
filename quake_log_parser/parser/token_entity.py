from enum import Enum


class Entity(str, Enum):
    UNKNOWN = "unknown"
    WORD = "word"
    DELIMITER = "delimiter"
    NUMBER = "number"
    TIME = "time"
    COMMAND = "command"
    COMMAND_ARGUMENT = "command_argument"
    KEYWORD = "keyword"
