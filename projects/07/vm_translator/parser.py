import enum
from typing import Iterator, Optional, Tuple, TextIO, Union


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
            command_class: Union[ArithmeticCommandClass, StackCommandClass],
            target_segment: Optional[str] = None,
            index: Optional[int] = None):
        self.command_class = command_class
        self.target_segment = target_segment
        self.index = index


class Parser:
    def __init__(self, file_obj: TextIO):
        self.file_obj = file_obj

    def parse_file(self) -> Iterator[Command]:
        for raw_command in self._get_raw_instructions():
            # Figure out the type of command
            yield self._inspect_raw_command(raw_command)

    def _get_raw_instructions(self) -> Iterator[Tuple[str]]:
        for line in self.file_obj:
            line = line.strip()
            if not line:
                # Empty line should be discarded
                continue

            if line.startswith('//'):
                # Comments should be discarded
                continue

            yield tuple(line.split())

    def _inspect_raw_command(self, raw_command: Tuple[str]) -> Command:
        number_of_elements = len(raw_command)
        if number_of_elements == 1:
            # Arithmetic
            return Command(command_class=ArithmeticCommandClass(raw_command[0]))
        elif number_of_elements == 3:
            # Stack operation
            return Command(
                command_class=StackCommandClass(raw_command[0]),
                target_segment=raw_command[1],
                index=int(raw_command[2])
            )
        else:
            raise ValueError(f"Unrecognized command {raw_command}")
