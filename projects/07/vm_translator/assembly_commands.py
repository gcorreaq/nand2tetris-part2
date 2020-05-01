from pathlib import Path
import uuid

from command import Command
from enumerations import MemorySegment


DOUBLE_ARG_ARITHMETIC_COMMAND_TO_OPERATOR = {
    'add': '+',
    'sub': '-',
    'and': '&',
    'or': '|',
}

SINGLE_ARG_ARITHMETIC_COMMAND_TO_OPERATOR = {
    'neg': '-',
    'not': '!',
}

COMPARISON_COMMAND_TO_OPERATOR = {
    'eq': 'JEQ',
    'gt': 'JGT',
    'lt': 'JLT',
}

STACK_POINTER_BASE_ADDRESS = '@R0  // SP: Stack Pointer'

MOVE_STACK_POINTER_UP = """
    {stack_pointer}
    M=M+1\t//SP++
""".format(stack_pointer=STACK_POINTER_BASE_ADDRESS)

MOVE_STACK_POINTER_DOWN = """
    {stack_pointer}
    M=M-1\t//SP--
""".format(stack_pointer=STACK_POINTER_BASE_ADDRESS)


POP_VALUE_ON_TOP_OF_STACK = """
    {stack_pointer}
    M=M-1  // SP--  -> Move stored address to top element of stack
    A=M    // Point to top of stack
    D=M    // Store value on top of stack
""".format(stack_pointer=STACK_POINTER_BASE_ADDRESS)

PUSH_VALUE_ON_TOP_OF_STACK = """
    {stack_pointer}
    A=M    // Point to the current top of the stack 
    M=D    // Modify top of stack by storing D (*SP = DATA)
    
    {stack_pointer}
    M=M+1  // SP++ -> Move stored address to above of top of stack
""".format(stack_pointer=STACK_POINTER_BASE_ADDRESS)


TWO_OPERANDS_POP_OPERATIONS = """
    //
    // BEGIN: TWO_OPERANDS_POP_OPERATIONS
    // Pop two operands from the stack and get them ready to be operated
    //

    {pop_top_of_stack}

    @second_operand
    M=D    // Keep value on top of stack in second_operand

    {pop_top_of_stack}
    
    @first_operand
    M=D    // Keep value on top of stack in first_operand

    //
    // END: TWO_OPERANDS_POP_OPERATIONS
    //
""".format(pop_top_of_stack=POP_VALUE_ON_TOP_OF_STACK)


class BaseArithmeticAssemblyCommand:
    assembly = ''
    command_mapping = {}

    def __init__(self, command: Command):
        self.command_name = command.command_class.value
        self.translated_operator = self.command_mapping[self.command_name]

    def __str__(self):
        return f"{type(self).__name__}<{self.command_name}>"

    def get_assembly(self) -> str:
        return self.assembly.format(
            operator=self.command_name,
            translated_operator=self.translated_operator,
            pop_two_operands=TWO_OPERANDS_POP_OPERATIONS,
            pop_from_stack=POP_VALUE_ON_TOP_OF_STACK,
            push_to_stack=PUSH_VALUE_ON_TOP_OF_STACK,
            unique_identifier=uuid.uuid4().int
        )


class TwoArgumentArithmeticCommand(BaseArithmeticAssemblyCommand):
    assembly = """
    // {operator}
    {pop_two_operands}

    @first_operand
    D=M

    @second_operand
    D=D{translated_operator}M  // We do: first_operand <OP> second_operand

    {push_to_stack}
    """
    command_mapping = DOUBLE_ARG_ARITHMETIC_COMMAND_TO_OPERATOR


class OneArgumentArithmeticCommand(BaseArithmeticAssemblyCommand):
    assembly = """
    // {operator}

    {pop_from_stack}

    D={translated_operator}D    // we get the data from top of stack, and we apply operator

    {push_to_stack}
    """
    command_mapping = SINGLE_ARG_ARITHMETIC_COMMAND_TO_OPERATOR


class ComparisonCommand(BaseArithmeticAssemblyCommand):
    assembly = """
    // {operator}
    
    {pop_two_operands}
    
    @first_operand
    D=M

    @second_operand
    D=D-M  // We take the difference between (first - second)
    
    @STORE_TRUE_{unique_identifier}
    D;{translated_operator}

    (STORE_FALSE_{unique_identifier})
        D=0
        @PUSH_RESULT_TO_STACK_{unique_identifier}
        0;JMP

    (STORE_TRUE_{unique_identifier})
        D=-1  // This sets all bits to 1
        @PUSH_RESULT_TO_STACK_{unique_identifier}
        0;JMP

    (PUSH_RESULT_TO_STACK_{unique_identifier})
        {push_to_stack}
    """
    command_mapping = COMPARISON_COMMAND_TO_OPERATOR


SEGMENT_ALIASES = {
    MemorySegment.LOCAL: 'R1',
    MemorySegment.ARG: 'R2',
    MemorySegment.THIS: 'R3',
    MemorySegment.THAT: 'R4',
    MemorySegment.TEMP: 'R5',
}


def _get_real_address_calculation(index: int) -> str:
    if index == 0:
        offset = "A=M"
    else:
        offset = "A=M+1"
        for repetitions in range(index - 1):
            offset += "\n    A=A+1"

    return offset


class BasePopPushLocalCommand:
    assembly = ''

    def __init__(self, command: Command):
        self.index = command.index
        self.segment = SEGMENT_ALIASES[command.target_segment]
        self.segment_name = command.target_segment.value

    def get_assembly(self) -> str:
        return self.assembly.format(
            index=self.index,
            segment=self.segment,
            segment_name=self.segment_name,
            address_calculation=_get_real_address_calculation(self.index),
            push_to_stack=PUSH_VALUE_ON_TOP_OF_STACK,
            pop_from_stack=POP_VALUE_ON_TOP_OF_STACK,
        )


class PushLocalCommand(BasePopPushLocalCommand):
    assembly = """
    // push {segment_name} {index}

    @{segment}
    {address_calculation}
    D=M   // D stores the value of *segment[index]

    {push_to_stack}
    """


class PopLocalCommand(BasePopPushLocalCommand):
    assembly = """
    // pop {segment_name} {index}

    {pop_from_stack}

    @{segment}
    {address_calculation}
    M=D    //  *addr = *sp
    """


class BasePopPushStaticCommand:
    assembly = ''

    def __init__(self, command: Command, filename: Path):
        self.index = command.index
        self.filename = filename

    def get_assembly(self) -> str:
        return self.assembly.format(
            index=self.index,
            filename=self.filename.stem,
            push_to_stack=PUSH_VALUE_ON_TOP_OF_STACK,
            pop_from_stack=POP_VALUE_ON_TOP_OF_STACK,
        )


class PushStaticCommand(BasePopPushStaticCommand):
    assembly = """
    // push static {index}

    @{filename}.{index}
    D=M   // D = *filename.index

    {push_to_stack}
    """


class PopStaticCommand(BasePopPushStaticCommand):
    assembly = """
    // pop static {index}

    {pop_from_stack}

    @{filename}.{index}
    M=D    //  *addr = *sp
    """


class PushConstantCommand:
    assembly = """
    // push constant {value}

    @{value}
    D=A

    {push_to_stack}
    """

    def __init__(self, command: Command):
        self.value = command.index

    def get_assembly(self) -> str:
        return self.assembly.format(
            value=self.value,
            push_to_stack=PUSH_VALUE_ON_TOP_OF_STACK,
        )


class BasePopPushTempCommand:
    assembly = ''

    def __init__(self, command: Command):
        self.index = command.index

    def _get_real_address(self):
        offset = ""
        if self.index > 0:
            for repetition in range(self.index):
                offset += "\n    A=A+1"

        return offset

    def get_assembly(self) -> str:
        return self.assembly.format(
            index=self.index,
            segment=SEGMENT_ALIASES[MemorySegment.TEMP],
            address_calculation=self._get_real_address(),
            pop_from_stack=POP_VALUE_ON_TOP_OF_STACK,
            push_to_stack=PUSH_VALUE_ON_TOP_OF_STACK,
        )


class PushTempCommand(BasePopPushTempCommand):
    assembly = """
    // push temp {index}
    
    @{segment}
    {address_calculation}
    D=M   // D stores the value of *segment[index]

    {push_to_stack}
    """


class PopTempCommand(BasePopPushTempCommand):
    assembly = """
    // pop temp {index}

    {pop_from_stack}

    @{segment}
    {address_calculation}
    M=D   // addr = *segment[i]
    """


class BasePopPushPointerCommand:
    INDEX_TO_SEGMENT_MAPPING = {
        0: SEGMENT_ALIASES[MemorySegment.THIS],
        1: SEGMENT_ALIASES[MemorySegment.THAT]
    }

    assembly = ''

    def __init__(self, command: Command):
        self.index = command.index
        self.segment = self.INDEX_TO_SEGMENT_MAPPING[self.index]

    def get_assembly(self) -> str:
        return self.assembly.format(
            index=self.index,
            segment=self.segment,
            pop_from_stack=POP_VALUE_ON_TOP_OF_STACK,
            push_to_stack=PUSH_VALUE_ON_TOP_OF_STACK,
        )


class PushPointerCommand(BasePopPushPointerCommand):
    assembly = """
    // push pointer {index}

    @{segment}
    D=M   // Get the value stored in THIS/THAT

    {push_to_stack}
    """


class PopPointerCommand(BasePopPushPointerCommand):
    assembly = """
    // pop temp {index}

    {pop_from_stack}

    @{segment}
    M=D   // Store in THIS/THAT what was in the top of the stack 
    """
