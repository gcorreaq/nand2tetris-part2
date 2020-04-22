from typing import Iterator, Tuple, TextIO

from command import Command


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
        if number_of_elements not in {1, 3}:
            raise ValueError(
                f"Invalid command length ({number_of_elements}) for {raw_command}"
            )

        return Command(*raw_command)
