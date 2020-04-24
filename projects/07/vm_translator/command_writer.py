from pathlib import Path
from typing import Iterable

import assembly_commands
from command import ArithmeticCommandClass, Command, StackCommandClass

COMMAND_TO_ASSEMBLY = {
    ArithmeticCommandClass.ADD: assembly_commands.TwoArgumentArithmeticCommand,
    ArithmeticCommandClass.SUB: assembly_commands.TwoArgumentArithmeticCommand,
    ArithmeticCommandClass.AND: assembly_commands.TwoArgumentArithmeticCommand,
    ArithmeticCommandClass.OR: assembly_commands.TwoArgumentArithmeticCommand,
    ArithmeticCommandClass.NEG: assembly_commands.OneArgumentArithmeticCommand,
    ArithmeticCommandClass.NOT: assembly_commands.OneArgumentArithmeticCommand,
    ArithmeticCommandClass.EQ: assembly_commands.ComparisonCommand,
    ArithmeticCommandClass.GT: assembly_commands.ComparisonCommand,
    ArithmeticCommandClass.LT: assembly_commands.ComparisonCommand,
}

MEMORY_COMMANDS_TO_SEGMENT_AND_ASSEMBLY = {
    StackCommandClass.POP: {
        'local': assembly_commands.PopLocalCommand,
        'static': assembly_commands.PopStaticCommand,
        'temp': assembly_commands.PopTempCommand,
        'pointer': assembly_commands.PopPointerCommand,
    },
    StackCommandClass.PUSH: {
        'local': assembly_commands.PushLocalCommand,
        'static': assembly_commands.PushStaticCommand,
        'constant': assembly_commands.PushConstantCommand,
        'temp': assembly_commands.PushTempCommand,
        'pointer': assembly_commands.PushPointerCommand
    },
}


class CommandWriter:

    def __init__(self, original_filename: str, commands: Iterable[Command]):
        self.original_filename = Path(original_filename)
        self.commands = commands

    def write_file(self):
        output_filename = self.original_filename.with_suffix('.asm')
        with output_filename.open(mode='w') as file_obj:
            file_obj.writelines(self.compile())

    def compile(self):
        for command in self.commands:
            if isinstance(command.command_class, ArithmeticCommandClass):
                yield self._process_arithmetic_command(command)
            else:
                yield self._process_memory_command(command)

    def _process_arithmetic_command(self, command: Command) -> str:
        assembly_compiler_class = COMMAND_TO_ASSEMBLY[command.command_class]
        assembly_compiler = assembly_compiler_class(command)
        return assembly_compiler.get_assembly()

    def _process_memory_command(self, command: Command) -> str:
        assembly_compiler_class = MEMORY_COMMANDS_TO_SEGMENT_AND_ASSEMBLY[command.command_class][command.target_segment]

        if isinstance(assembly_compiler_class, assembly_commands.BasePopPushStaticCommand):
            assembly_compiler = assembly_compiler_class(command, self.original_filename)
        else:
            assembly_compiler = assembly_compiler_class(command)

        return assembly_compiler.get_assembly()
