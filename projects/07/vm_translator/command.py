import enum
from typing import Optional


class ArithmeticCommandClass(enum.Enum):
    ADD = 'add'
    SUB = 'sub'
    NEG = 'neg'
    EQ = 'eq'
    GT = 'gt'
    LT = 'lt'
    AND = 'and'
    OR = 'or'
    NOT = 'not'


class StackCommandClass(enum.Enum):
    POP = 'pop'
    PUSH = 'push'


class Command:
    def __init__(
            self,
            command_class: str,
            target_segment: Optional[str] = None,
            index: Optional[int] = None):
        self.target_segment = target_segment
        self.index = self._parse_and_validate_index(index)
        self.command_class = self._parse_and_validate_command_class(command_class)

    def _parse_and_validate_index(self, index):
        if index is None:
            return None

        index = int(index)
        if index < 0:
            raise ValueError(f'Invalid memory index {index}')
        return index

    def _parse_and_validate_command_class(self, command_class):
        if self.target_segment is not None and self.index is not None:
            return StackCommandClass(command_class)
        elif self.target_segment is None and self.index is None:
            return ArithmeticCommandClass(command_class)
        else:
            raise ValueError(f'Invalid command: {command_class=} {self.target_segment=} {self.index=}')
