import enum


class DifficultyEnum(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"
    special = "special"


class LanguageEnum(str, enum.Enum):
    python = "python"
