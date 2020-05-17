import logging
from pathlib import Path
from typing import Iterable, TextIO

from assembly_commands import (
    AssemblyCommand,
    BasePopPushStaticCommand,
    CallFunctionCommand,
    ComparisonCommand,
    FunctionCommand,
    GoToLabelCommand,
    IfGoToLabelCommand,
    LabelCommand,
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
    ReturnCommand,
    TwoArgumentArithmeticCommand,
)
from command import Command
from enumerations import (
    ArithmeticCommandClass,
    BranchCommandClass,
    FunctionCommandClass,
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
    BranchCommandClass.GOTO: GoToLabelCommand,
    BranchCommandClass.IF_GOTO: IfGoToLabelCommand,
    BranchCommandClass.LABEL: LabelCommand,
    FunctionCommandClass.CALL: CallFunctionCommand,
    FunctionCommandClass.FUNCTION: FunctionCommand,
    FunctionCommandClass.RETURN: ReturnCommand,
}

MEMORY_COMMANDS_TO_SEGMENT_AND_ASSEMBLY = {
    StackCommandClass.POP: {
        MemorySegment.LOCAL: PopLocalCommand,
        MemorySegment.ARG: PopLocalCommand,
        MemorySegment.THIS: PopLocalCommand,
        MemorySegment.THAT: PopLocalCommand,
        MemorySegment.STATIC: PopStaticCommand,
        MemorySegment.TEMP: PopTempCommand,
        MemorySegment.POINTER: PopPointerCommand,
    },
    StackCommandClass.PUSH: {
        MemorySegment.LOCAL: PushLocalCommand,
        MemorySegment.ARG: PushLocalCommand,
        MemorySegment.THIS: PushLocalCommand,
        MemorySegment.THAT: PushLocalCommand,
        MemorySegment.STATIC: PushStaticCommand,
        MemorySegment.CONSTANT: PushConstantCommand,
        MemorySegment.TEMP: PushTempCommand,
        MemorySegment.POINTER: PushPointerCommand
    },
}


logger = logging.getLogger("vm_translator.command_writer")


def _process_arithmetic_command(command: Command) -> AssemblyCommand:
    assembly_compiler_class = COMMAND_TO_ASSEMBLY[command.command_class]
    assembly_compiler = assembly_compiler_class(command)
    return assembly_compiler


def _process_branch_command(command: Command, input_filename: Path) -> AssemblyCommand:
    assembly_compiler_class = COMMAND_TO_ASSEMBLY[command.command_class]
    assembly_compiler = assembly_compiler_class(command, input_filename)
    return assembly_compiler


def _process_function_command(command: Command, input_filename: Path, function_call_counter: int) -> AssemblyCommand:
    assembly_compiler_class = COMMAND_TO_ASSEMBLY[command.command_class]
    if issubclass(assembly_compiler_class, CallFunctionCommand):
        assembly_compiler = assembly_compiler_class(command, input_filename, function_call_counter)
    else:
        assembly_compiler = assembly_compiler_class(command, input_filename)
    return assembly_compiler


def _process_memory_command(command: Command, original_filename: Path) -> AssemblyCommand:
    assembly_compiler_class = MEMORY_COMMANDS_TO_SEGMENT_AND_ASSEMBLY[command.command_class][command.target_segment]
    logger.debug(
        'Command %s for segment %s match to assembly compiler %s',
        command,
        command.target_segment,
        assembly_compiler_class
    )

    if issubclass(assembly_compiler_class, BasePopPushStaticCommand):
        assembly_compiler = assembly_compiler_class(command, original_filename)
    else:
        assembly_compiler = assembly_compiler_class(command)

    return assembly_compiler


class CommandWriter:

    def __init__(self, output_file: TextIO, input_file_path: Path, commands: Iterable[Command]):
        self.output_file = output_file
        self.input_filename = input_file_path
        self.output_filename = self.output_file.name
        self.commands = commands

    def compile(self):
        logger.info('Compiling commands into file %s', self.output_filename)
        self.output_file.writelines(self._translate_commands())

    def _translate_commands(self):
        function_call_counter = 0
        for command in self.commands:
            logger.debug('Command %s is of type %r', command, command.command_class)
            if isinstance(command.command_class, ArithmeticCommandClass):
                assembly_compiler = _process_arithmetic_command(command)
            elif isinstance(command.command_class, BranchCommandClass):
                assembly_compiler = _process_branch_command(command, self.input_filename)
            elif isinstance(command.command_class, FunctionCommandClass):
                if command.command_class == FunctionCommandClass.CALL:
                    function_call_counter += 1
                elif command.command_class == FunctionCommandClass.RETURN:
                    function_call_counter = 0
                assembly_compiler = _process_function_command(
                    command,
                    self.input_filename,
                    function_call_counter
                )
            else:
                assembly_compiler = _process_memory_command(command, self.input_filename)

            logger.debug('Command %s is assembly command %s', command, assembly_compiler)
            assembly_string = assembly_compiler.get_assembly()
            logger.debug('Result of compiling command %s is %r', command, assembly_string)
            yield assembly_string
