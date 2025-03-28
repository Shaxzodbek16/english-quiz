from enum import Enum


class TestTypeEnum(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    GAP_FILLING = "gap_filling"

    @classmethod
    def get_elements_as_list(cls) -> list[str]:
        return [item.value for item in cls]
