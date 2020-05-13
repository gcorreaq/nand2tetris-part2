from typing import Optional

from enumerations import (
    CommandClass,
    COMMAND_TO_COMMAND_CLASS_MEMBER,
    MemorySegment,
)


class Command:
    def __init__(
            self,
            arg0: str,
            arg1: Optional[str] = None,
            arg2: Optional[str] = None):
        self.arg0 = arg0
        self.arg1 = arg1
        self.arg2: Optional[int] = self._parse_and_validate_arg2(arg2)
        self.command_class: CommandClass = self._parse_and_validate_command_class()
        self.target_segment: Optional[MemorySegment] = self._parse_and_validate_segment()
        self.index: Optional[int] = self.arg2

    def __str__(self):
        if self.target_segment is None and self.index is None:
            return f"Command<{self.command_class}>"
        else:
            return f"Command<{self.command_class} {self.target_segment} INDEX.{self.index}>"

    def _parse_and_validate_segment(self):
        if self.arg1 is None:
            return None

        if isinstance(self.command_class, CommandClass):
            return MemorySegment(self.arg1)

    def _parse_and_validate_arg2(self, raw_arg2):
        if raw_arg2 is None:
            return None

        arg2 = int(raw_arg2)
        if arg2 < 0:
            raise ValueError(f'Invalid value for arg2: {arg2}')
        return arg2

    def _parse_and_validate_command_class(self):
        try:
            return COMMAND_TO_COMMAND_CLASS_MEMBER[self.arg0]
        except KeyError:
            raise ValueError(f'Invalid command: {self.arg0} {self.arg1} {self.arg2}')
