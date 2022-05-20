from enum import Enum


class JSONDecodeErrors(Enum):
    ALL_OK = 0
    INVALID_JSON = 1
    NO_SCHEMA = 2
