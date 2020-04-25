import logging
from pathlib import Path
from typing import Iterable

from assembly_commands import (
    BasePopPushStaticCommand,
    ComparisonCommand,
    OneArgumentArithmeticCommand,
    PopLocalCommand,
    PopPointerCommand,
    PopStaticCommand,
    PopTempCommand,
    PushConstantCommand,
    PushLocalCommand,
    PushPointerCommand,
    PushStaticCommand,
    PushTempCommand,
    TwoArgumentArithmeticCommand,
)
from command import Command
from enumerations import (
    ArithmeticCommandClass,
    MemorySegment,
    StackCommandClass,
)

COMMAND_TO_ASSEMBLY = {
    ArithmeticCommandClass.ADD: TwoArgumentArithmeticCommand,
    ArithmeticCommandClass.SUB: TwoArgumentArithmeticCommand,
    ArithmeticCommandClass.AND: TwoArgumentArithmeticCommand,
    ArithmeticCommandClass.OR: TwoArgumentArithmeticCommand,
    ArithmeticCommandClass.NEG: OneArgumentArithmeticCommand,
    ArithmeticCommandClass.NOT: OneArgumentArithmeticCommand,
    ArithmeticCommandClass.EQ: ComparisonCommand,
    ArithmeticCommandClass.GT: ComparisonCommand,
    ArithmeticCommandClass.LT: ComparisonCommand,
}

MEMORY_COMMANDS_TO_SEGMENT_AND_ASSEMBLY = {
    StackCommandClass.POP: {
        MemorySegment.LOCAL: PopLocalCommand,
        MemorySegment.STATIC: PopStaticCommand,
        MemorySegment.TEMP: PopTempCommand,
        MemorySegment.POINTER: PopPointerCommand,
    },
    StackCommandClass.PUSH: {
        MemorySegment.LOCAL: PushLocalCommand,
        MemorySegment.STATIC: PushStaticCommand,
        MemorySegment.CONSTANT: PushConstantCommand,
        MemorySegment.TEMP: PushTempCommand,
        MemorySegment.POINTER: PushPointerCommand
    },
}


logger = logging.getLogger(__name__)


def _process_arithmetic_command(command: Command) -> str:
    assembly_compiler_class = COMMAND_TO_ASSEMBLY[command.command_class]
    assembly_compiler = assembly_compiler_class(command)
    logger.debug('Command %s is assembly command %s', command, assembly_compiler)
    assembly_string = assembly_compiler.get_assembly()
    logger.debug('Result of compiling command %s is %r', command, assembly_string)
    return assembly_string


def _process_memory_command(command: Command, original_filename: Path) -> str:
    assembly_compiler_class = MEMORY_COMMANDS_TO_SEGMENT_AND_ASSEMBLY[command.command_class][command.target_segment]

    if isinstance(assembly_compiler_class, BasePopPushStaticCommand):
        assembly_compiler = assembly_compiler_class(command, original_filename)
    else:
        assembly_compiler = assembly_compiler_class(command)
    logger.debug('Command %s is assembly command %s', command, assembly_compiler)
    assembly_string = assembly_compiler.get_assembly()
    logger.debug('Result of compiling command %s is %r', command, assembly_string)
    return assembly_string


class CommandWriter:

    def __init__(self, original_filename: Path, commands: Iterable[Command]):
        self.original_filename = original_filename
        self.commands = commands

    def compile(self):
        output_filename = self.original_filename.with_suffix('.asm')
        logger.info(
            'Compiling commands from file %s into file %s',
            self.original_filename,
            output_filename
        )
        with output_filename.open(mode='w') as file_obj:
            file_obj.writelines(self._translate_commands())

    def _translate_commands(self):
        for command in self.commands:
            if isinstance(command.command_class, ArithmeticCommandClass):
                logger.debug('Command %s is of type Arithmetic', command)
                yield _process_arithmetic_command(command)
            else:
                logger.debug('Command %s is of type Memory', command)
                yield _process_memory_command(command, self.original_filename)
