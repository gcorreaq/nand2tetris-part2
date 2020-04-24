from command import Command


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

STACK_POINTER_BASE_ADDRESS = '@R0'


class BaseArithmeticAssemblyCommand:
    assembly = ''
    command_mapping = {}

    def __init__(self, command: Command):
        self.command_name = command.command_class.value
        self.translated_operator = self.command_mapping[self.command_name]

    def get_assembly(self):
        return self.assembly.format(
            stack_pointer=STACK_POINTER_BASE_ADDRESS,
            operator=self.command_name,
            translated_operator=self.translated_operator
        )


class TwoArgumentArithmeticCommand(BaseArithmeticAssemblyCommand):
    assembly = """
    // {operator}

    {stack_pointer}
    M=M-1  // SP--
    A=M    // *sp is in top of stack
    @second_operand
    D=M    // we get the data from top of stack

    {stack_pointer}
    M=M-1  // SP--
    A=M    // *sp is in top of stack
    @first_operand
    D=M

    @second_operand
    D=D{translated_operator}M  // We do: first OP second

    {stack_pointer}
    A=M
    M=D   // Store result in top of stack

    {stack_pointer}
    M=M+1  // Move stack pointer one position up
    """
    command_mapping = DOUBLE_ARG_ARITHMETIC_COMMAND_TO_OPERATOR


class OneArgumentArithmeticCommand(BaseArithmeticAssemblyCommand):
    assembly = """
    // {operator}

    {stack_pointer}
    M=M-1  // SP--
    A=M    // *sp is in top of stack
    @operand
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
    
    {stack_pointer}
    M=M-1  // SP--
    A=M    // *sp is in top of stack
    @second_operand
    D=M    // we get the data from top of stack

    {stack_pointer}
    M=M-1  // SP--
    A=M    // *sp is in top of stack
    @first_operand
    D=M

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
    'local': 'R1',
    'arg': 'R2',
    'this': 'R3',
    'that': 'R4',
    'temp': 'R5'
}


class BaseMemoryCommand:
    assembly = ''

    def __init__(self, command: Command):
        self.segment = command.target_segment
        self.index = command.index

    def get_assembly(self):
        return self.assembly.format(
            stack_pointer=STACK_POINTER_BASE_ADDRESS,
            segment_base_address=self.segment,
            index=self.index
        )


class PushLocalCommand:
    assembly = """
    // push local {index}

    @{segment}
    D=M+{index}   // Get the address where the index is
    @addr
    M=D   // addr = *segment[i]
    D=M   // D stores what *addr is pointing to

    {stack_pointer}
    A=M  // Now pointing to top of stack
    M=D  // *sp = *addr

    {stack_pointer}
    M=M+1  // SP++
    """

    def __init__(self, command: Command):
        self.index = command.index

    def get_assembly(self):
        return self.assembly.format(
            stack_pointer=STACK_POINTER_BASE_ADDRESS,
            index=self.index,
            segment=SEGMENT_ALIASES['local']
        )


class PopLocalCommand:
    assembly = """
    // pop local {index}

    @{segment}
    D=M+{index}  // Get the address where index is 
    @addr
    M=D   // addr = *segment[i]

    {stack_pointer}
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @addr
    A=M
    M=D    //  *addr = *sp
    """

    def __init__(self, command: Command):
        self.index = command.index

    def get_assembly(self):
        return self.assembly.format(
            stack_pointer=STACK_POINTER_BASE_ADDRESS,
            index=self.index,
            segment=SEGMENT_ALIASES['local']
        )


class BasePopPushStaticCommand:
    assembly = ''

    def __init__(self, command: Command, filename: str):
        self.index = command.index
        self.filename = filename

    def get_assembly(self):
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

    {stack_pointer}
    A=M  // Now pointing to top of stack
    M={value}  // *sp = constant

    {stack_pointer}
    M=M+1  // SP++
    """

    def __init__(self, command: Command):
        self.index = command.index

    def get_assembly(self):
        return self.assembly.format(
            stack_pointer=STACK_POINTER_BASE_ADDRESS,
            index=self.index
        )


class BasePopPushTempCommand:
    assembly = ''

    def __init__(self, command: Command):
        self.index = command.index

    def get_assembly(self):
        return self.assembly.format(
            stack_pointer=STACK_POINTER_BASE_ADDRESS,
            index=self.index,
            segment=SEGMENT_ALIASES['temp']
        )


class PushTempCommand(BasePopPushTempCommand):
    assembly = """
    // push temp {index}
    
    @{segment}
    D=M+{index}   // Get the address where the index is
    @addr
    M=D   // addr = *segment[i]
    D=M   // D stores what *addr is pointing to

    {stack_pointer}
    A=M  // Now pointing to top of stack
    M=D  // *sp = *addr

    {stack_pointer}
    M=M+1  // SP++
    """


class PopTempCommand(BasePopPushTempCommand):
    assembly = """
    // pop temp {index}

    @{segment}
    D=M+{index}  // Get the address where index is 
    @addr
    M=D   // addr = *segment[i]

    {stack_pointer}
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @addr
    A=M
    M=D    //  *addr = *sp
    """


class BasePopPushPointerCommand:
    INDEX_TO_SEGMENT_MAPPING = {
        0: SEGMENT_ALIASES['this'],
        1: SEGMENT_ALIASES['that']
    }

    assembly = ''

    def __init__(self, command: Command):
        self.index = command.index
        self.segment = self.INDEX_TO_SEGMENT_MAPPING[self.index]

    def get_assembly(self):
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
