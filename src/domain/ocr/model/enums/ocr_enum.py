from enum import StrEnum, auto


class OcrLangEnum(StrEnum):
    ENG = auto()
    KOR = auto()

    @classmethod
    def to_list(cls):
        return [v.value for v in cls]
