from typing import Optional, Union

from enumerations import (
    ArithmeticCommandClass,
    MemorySegment,
    StackCommandClass,
)


class Command:
    def __init__(
            self,
            command_class: str,
            target_segment: Optional[str] = None,
            index: Optional[str] = None):
        self.target_segment: MemorySegment = self._parse_and_validate_segment(target_segment)
        self.index: int = self._parse_and_validate_index(index)
        self.command_class: Union[ArithmeticCommandClass, StackCommandClass] = self._parse_and_validate_command_class(command_class)

    def __str__(self):
        if self.target_segment is None and self.index is None:
            return f"Command<{self.command_class}>"
        else:
            return f"Command<{self.command_class} {self.target_segment} INDEX.{self.index}>"

    def _parse_and_validate_segment(self, segment: Optional[str]):
        if segment is None:
            return None

        return MemorySegment(segment)

    def _parse_and_validate_index(self, index: Optional[str]):
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
            raise ValueError(f'Invalid command: {command_class} {self.target_segment} {self.index}')
