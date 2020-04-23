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


class PopCommand:
    assembly = """
    // pop {segment} {index}

    @{segment_base_address}
    D=M+{index}  // Get the address where index is 
    @addr
    M=D   // addr = *segment[i]

    @SP
    M=M-1  // SP--
    A=M    // Stack pointer now in top element
    D=M    // Store whatever the top of the stack had

    @addr
    M=D    //  *addr = *sp
    """


class PushCommand:
    assembly = """
    // push {segment} {index}

    @{segment_base_address}
    D=M+{index}   // Get the address where the index is
    @addr
    M=D   // addr = *segment[i]
    D=M   // D stores what *addr is pointing to

    @SP
    A=M  // Now pointing to top of stack
    M=D  // *sp = *addr

    @SP
    M=M+1  // SP++
    """


class TwoArgumentArithmeticCommand:
    assembly = """
    // {operator}

    @SP
    M=M-1  // SP--
    A=M    // *sp is in top of stack
    @second_operand
    D=M    // we get the data from top of stack

    @SP
    M=M-1  // SP--
    A=M    // *sp is in top of stack
    @first_operand
    D=M

    @second_operand
    D=D{translated_operator}M  // We do: first OP second

    @SP
    A=M
    M=D   // Store result in top of stack

    @SP
    M=M+1  // Move stack pointer one position up
    """

    def __init__(self, command: Command):
        self.command_name = command.command_class.value
        self.translated_operator = DOUBLE_ARG_ARITHMETIC_COMMAND_TO_OPERATOR[self.command_name]

    def get_assembly(self):
        return self.assembly.format(
            operator=self.command_name,
            translated_operator=self.translated_operator
        )
