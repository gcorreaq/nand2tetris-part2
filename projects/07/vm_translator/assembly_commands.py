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

MOVE_STACK_POINTER_DOWN = """{stack_pointer}
    M=M-1\t//SP--
""".format(stack_pointer=STACK_POINTER_BASE_ADDRESS)

TWO_OPERANDS_POP_OPERATIONS = """
    //
    // BEGIN: TWO_OPERANDS_POP_OPERATIONS
    // Pop two operands from the stack and get them ready to be operated
    //

    {stack_pointer_down}
    A=M\t\t// *sp is in top of stack
    D=M\t\t// Get value on top of stack

    @second_operand
    M=D\t\t// Keep value on top of stack in second_operand

    {stack_pointer_down}
    A=M\t\t// *sp is in top of stack
    D=M\t\t// Get value on top of stack

    //
    // END: TWO_OPERANDS_POP_OPERATIONS
    //
""".format(stack_pointer_down=MOVE_STACK_POINTER_DOWN)


class BaseArithmeticAssemblyCommand:
    assembly = ''
    command_mapping = {}

    def __init__(self, command: Command):
        self.command_name = command.command_class.value
        self.translated_operator = self.command_mapping[self.command_name]

    def __str__(self):
        return f"{self.__name__}<{self.command_name}>"

    def get_assembly(self) -> str:
        return self.assembly.format(
            stack_pointer=STACK_POINTER_BASE_ADDRESS,
            operator=self.command_name,
            translated_operator=self.translated_operator,
            pop_two_operands=TWO_OPERANDS_POP_OPERATIONS
        )


class TwoArgumentArithmeticCommand(BaseArithmeticAssemblyCommand):
    assembly = """
    // {operator}
    {pop_two_operands}

    @second_operand
    D=D{translated_operator}M\t// We do: first OP second

    {stack_pointer}
    A=M
    M=D\t\t// Store result in top of stack

    {stack_pointer}
    M=M+1\t// Move stack pointer one position up
    """
    command_mapping = DOUBLE_ARG_ARITHMETIC_COMMAND_TO_OPERATOR


class OneArgumentArithmeticCommand(BaseArithmeticAssemblyCommand):
    assembly = """
    // {operator}

    {stack_pointer}
    M=M-1  // SP--
    A=M    // *sp is in top of stack

    D={translated_operator}M    // we get the data from top of stack, and we apply operator

    {stack_pointer}
    A=M
    M=D   // Store result in top of stack

    {stack_pointer}
    M=M+1  // Move stack pointer one position up
    """
    command_mapping = SINGLE_ARG_ARITHMETIC_COMMAND_TO_OPERATOR


class ComparisonCommand(BaseArithmeticAssemblyCommand):
    assembly = """
    // {operator}
    
    {pop_two_operands}

    @second_operand
    D=D-M  // We take the difference between (first - second)
    
    @STORE_TRUE
    D;{translated_operator}
    
    (STORE_FALSE)
        D=0
        @PUSH_RESULT_TO_STACK
        0;JMP
    
    (STORE_TRUE)
        D=-1  // This sets all bits to 1
        @PUSH_RESULT_TO_STACK
        0;JMP
        
    (PUSH_RESULT_TO_STACK)
        {stack_pointer}
        A=M  // Point to where the top is
        M=D  // Set the top to new value
        
        {stack_pointer}
        M=M+1  // Move top one position up
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
            stack_pointer=STACK_POINTER_BASE_ADDRESS,
            index=self.index,
            segment=self.segment,
            segment_name=self.segment_name,
            address_calculation=_get_real_address_calculation(self.index)
        )


class PushLocalCommand(BasePopPushLocalCommand):
    assembly = """
    // push {segment_name} {index}

    @{segment}
    {address_calculation}
    D=M   // D stores the value of *segment[index]

    {stack_pointer}
    A=M  // Now pointing to top of stack
    M=D  // *sp = *segment[index]

    {stack_pointer}
    M=M+1  // SP++
    """


class PopLocalCommand(BasePopPushLocalCommand):
    assembly = """
    // pop {segment_name} {index}

    {stack_pointer}
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @{segment}
    {address_calculation}
    M=D    //  *addr = *sp
    """


class BasePopPushStaticCommand:
    assembly = ''

    def __init__(self, command: Command, filename: str):
        self.index = command.index
        self.filename = filename

    def get_assembly(self) -> str:
        return self.assembly.format(
            stack_pointer=STACK_POINTER_BASE_ADDRESS,
            index=self.index,
            filename=self.filename
        )


class PushStaticCommand(BasePopPushStaticCommand):
    assembly = """
    // push static {index}

    @{filename}.{index}
    D=M   // D = *filename.index

    {stack_pointer}
    A=M  // Now pointing to top of stack
    M=D  // *sp = *filename.index

    {stack_pointer}
    M=M+1  // SP++
    """


class PopStaticCommand(BasePopPushStaticCommand):
    assembly = """
    // pop static {index}

    {stack_pointer}
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @{filename}.{index}
    M=D    //  *addr = *sp
    """


class PushConstantCommand:
    assembly = """
    // push constant {value}

    @{value}
    D=A

    {stack_pointer}
    A=M
    M=D

    {stack_pointer}
    M=M+1  // SP++
    """

    def __init__(self, command: Command):
        self.value = command.index

    def get_assembly(self) -> str:
        return self.assembly.format(
            stack_pointer=STACK_POINTER_BASE_ADDRESS,
            value=self.value
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
            stack_pointer=STACK_POINTER_BASE_ADDRESS,
            index=self.index,
            segment=SEGMENT_ALIASES[MemorySegment.TEMP],
            address_calculation=self._get_real_address()
        )


class PushTempCommand(BasePopPushTempCommand):
    assembly = """
    // push temp {index}
    
    @{segment}
    {address_calculation}
    D=M   // D stores the value of *segment[index]

    {stack_pointer}
    A=M  // Now pointing to top of stack
    M=D  // *sp = *addr

    {stack_pointer}
    M=M+1  // SP++
    """


class PopTempCommand(BasePopPushTempCommand):
    assembly = """
    // pop temp {index}

    {stack_pointer}
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

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
            stack_pointer=STACK_POINTER_BASE_ADDRESS,
            index=self.index,
            segment=self.segment
        )


class PushPointerCommand(BasePopPushPointerCommand):
    assembly = """
    // push pointer {index}

    @{segment}
    D=M   // Get the value stored in THIS/THAT

    {stack_pointer}
    A=M  // Now pointing to top of stack
    M=D  // Store in top of stack the value of THIS/THAT

    {stack_pointer}
    M=M+1  // SP++
    """


class PopPointerCommand(BasePopPushPointerCommand):
    assembly = """
    // pop temp {index}

    {stack_pointer}
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @{segment}
    M=D   // Store in THIS/THAT what was in the top of the stack 
    """
