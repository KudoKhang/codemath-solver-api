import enum


class ProblemDifficultyEnum(int, enum.Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class ProgrammingLanguageEnum(int, enum.Enum):
    PYTHON = 1
    C = 2
    CPP = 3


class ContentFormatEnum(int, enum.Enum):
    MARKDOWN = 1
    PLAINTEXT = 2
    PDF_URL = 3
    IMG_URL = 4


class SolutionStatusEnum(int, enum.Enum):
    PENDING = 1
    ACCEPTED = 2
    WRONG_ANSWER = 3
    TIME_LIMIT_EXCEEDED = 4
    RUNTIME_ERROR = 5


class CodeFileTypeEnum(int, enum.Enum):
    TEXT = 1
    FILE = 2


class RoleEnum(int, enum.Enum):
    USER = 1
    EDITOR = 2
    ADMIN = 3


class PlatformEnum(int, enum.Enum):
    CODEMATH = 1
