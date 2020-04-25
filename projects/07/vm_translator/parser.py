import logging
from typing import Iterator, List, TextIO

from command import Command


logger = logging.getLogger("vm_translator.parser")


class Parser:
    def __init__(self, file_obj: TextIO):
        self.file_obj = file_obj

    def parse_file(self) -> Iterator[Command]:
        logger.info('Processing %s', self.file_obj)
        for raw_command in self._get_raw_instructions():
            # Figure out the type of command
            yield self._inspect_raw_command(raw_command)

    def _get_raw_instructions(self) -> Iterator[List[str]]:
        logger.info('Processing lines in file %s', self.file_obj)
        line_number = 0
        for line_number, line in enumerate(self.file_obj, start=1):
            logger.debug(
                'Processing line %d with raw contents: %r',
                line_number,
                line
            )
            line = line.strip()
            if not line:
                # Empty line should be discarded
                logger.debug('Line %d is considered empty', line_number)
                continue

            if line.startswith('//'):
                # Comments should be discarded
                logger.debug('Line %d is a comment', line_number)
                continue

            line_components = line.split()
            logger.debug(
                'Line %d split into components %r',
                line_number,
                line_components
            )
            yield line_components
        logger.info(
            'Processed %d lines in file %s',
            line_number,
            self.file_obj
        )

    def _inspect_raw_command(self, raw_command: List[str]) -> Command:
        logger.debug('Inspecting raw command %r', raw_command)
        number_of_elements = len(raw_command)
        if number_of_elements not in {1, 3}:
            raise ValueError(
                f"Invalid command length ({number_of_elements}) for {raw_command}"
            )

        command = Command(*raw_command)
        logger.debug('Created Command instance %s', command)
        return command
