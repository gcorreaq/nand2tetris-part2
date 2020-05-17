from pathlib import Path
from typing import Dict
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


class AssemblyCommand:
    assembly = ''

    def get_assembly(self) -> str:
        pass


class BaseArithmeticAssemblyCommand(AssemblyCommand):
    command_mapping: Dict[str, str] = {}

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


class BasePopPushLocalCommand(AssemblyCommand):
    def __init__(self, command: Command):
        self.index = command.index
        self.segment = SEGMENT_ALIASES[command.target_segment]
        self.segment_name = command.target_segment.value

    def get_assembly(self) -> str:
        return self.assembly.format(
            index=self.index,
            segment=self.segment,
            segment_name=self.segment_name,
            push_to_stack=PUSH_VALUE_ON_TOP_OF_STACK,
            pop_from_stack=POP_VALUE_ON_TOP_OF_STACK,
        )


class PushLocalCommand(BasePopPushLocalCommand):
    assembly = """
    // push {segment_name} {index}

    @{index}
    D=A

    @{segment}
    A=M+D  // Base address + offset (index) => SEGMENT[INDEX]
    D=M   // D stores the value of *segment[index]

    {push_to_stack}
    """


class PopLocalCommand(BasePopPushLocalCommand):
    assembly = """
    // pop {segment_name} {index}
    @{index}
    D=A
    
    @{segment}
    D=M+D
    @target_address
    M=D

    {pop_from_stack}

    @target_address
    A=M
    M=D    //  *addr = *sp
    """


class BasePopPushStaticCommand(AssemblyCommand):
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


class BasePopPushTempCommand(AssemblyCommand):
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

# TODO: Fix address calculation for <push temp> and <pop temp>

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


class BasePopPushPointerCommand(AssemblyCommand):
    INDEX_TO_SEGMENT_MAPPING = {
        0: SEGMENT_ALIASES[MemorySegment.THIS],
        1: SEGMENT_ALIASES[MemorySegment.THAT]
    }

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


LABEL_STANDARD_FORMAT = "{filename}.{function_name}${label_name}"


class BaseBranchCommand(AssemblyCommand):
    def __init__(self, command: Command, input_file_path: Path):
        self.filename = input_file_path.stem
        self.current_function_name = command.current_function_name
        self.command = command
        self.label_name = self.command.arg1

    def _get_label_tag(self) -> str:
        current_function_name = self.current_function_name
        if current_function_name is None:
            current_function_name = 'main'

        return LABEL_STANDARD_FORMAT.format(
            filename=self.filename,
            function_name=current_function_name,
            label_name=self.label_name
        )


class LabelCommand(BaseBranchCommand):
    assembly = """
    // label {label_name}

    ({label_tag})
    """

    def get_assembly(self) -> str:
        return self.assembly.format(
            label_name=self.label_name,
            label_tag=self._get_label_tag()
        )


class GoToLabelCommand(BaseBranchCommand):
    assembly = """
    // goto {label_name}

    @{label_tag}
    0;JMP  // Unconditional jump
    """

    def get_assembly(self) -> str:
        return self.assembly.format(
            label_name=self.label_name,
            label_tag=self._get_label_tag()
        )


class IfGoToLabelCommand(BaseBranchCommand):
    assembly = """
    // if-goto {label_name}
    
    {pop_from_stack}
    
    @{label_tag}
    D;JNE  // Jump only when DATA is different than zero (True)
    """

    def get_assembly(self) -> str:
        return self.assembly.format(
            label_name=self.label_name,
            pop_from_stack=POP_VALUE_ON_TOP_OF_STACK,
            label_tag=self._get_label_tag()
        )


class BaseFunctionCommand(AssemblyCommand):
    def __init__(self, command: Command, input_file_path: Path):
        self.command = command
        self.filename = input_file_path.stem
        self.current_function_name = self.command.current_function_name


class CallFunctionCommand(BaseFunctionCommand):
    assembly = """
    // call {function_name} {nargs}
    
    // Save frame
    // Save return address
    @{return_address_label}
    D=A
    {push_to_stack}
    
    // Save LCL
    @{lcl_address}
    D=A
    {push_to_stack}
    
    // Save ARG
    @{arg_address}
    D=A
    {push_to_stack}
    
    // Save THIS
    @{this_address}
    D=A
    {push_to_stack}
    
    // Save THAT
    @{that_address}
    D=A
    {push_to_stack}
    
    // Set ARG pointer
    @5  // We need to subtract 5, because of the 5 values that we pushed
    D=A
    @{nargs}  // How many args we have
    D=D-A
    {stack_pointer}
    D=M-D  // DATA equals to SP - 5 - nArgs
    @{arg_address}
    M=D   // arg = SP - nArgs
    
    // Set LCL pointer
    {stack_pointer}
    D=A
    @{lcl_address}
    M=D  // LCL = SP

    // Go unconditionally to the function being called
    @{file_name}.{function_name)
    0;JMP
   
    // We will return here after 
    ({return_address_label})
    """

    def __init__(self, command: Command, input_file_path: Path, function_call_count: int):
        super(CallFunctionCommand, self).__init__(command, input_file_path)
        self.function_call_count = function_call_count

    def _get_return_address_label(self):
        return "{file_name}.{function_name}$ret.{index}".format(
            file_name=self.filename,
            function_name=self.command.arg1,
            index=self.function_call_count
        )

    def get_assembly(self) -> str:
        return self.assembly.format(
            function_name=self.command.arg1,
            nvars=self.command.arg2,
            file_name=self.filename,
            return_address_label=self._get_return_address_label(),
            push_to_stack=PUSH_VALUE_ON_TOP_OF_STACK,
            stack_pointer=STACK_POINTER_BASE_ADDRESS,
            lcl_address=SEGMENT_ALIASES[MemorySegment.LOCAL],
            arg_address=SEGMENT_ALIASES[MemorySegment.ARG],
            this_address=SEGMENT_ALIASES[MemorySegment.THIS],
            that_address=SEGMENT_ALIASES[MemorySegment.THAT]
        )


class FunctionCommand(BaseFunctionCommand):
    assembly = """
    // function {function_name} {nvars}
    
    // Entry point
    ({file_name}.{function_name})
    
    // Set local segment by pushing zeros to the stack
    {set_local_segment}
    """

    def _get_setup_of_local_segment(self) -> str:
        base_command = ""
        push_constant_zero_assembly = PushConstantCommand(
            Command(arg0='push', arg1=MemorySegment.CONSTANT.value, arg2='0')
        ).get_assembly()

        for local_var_index in range(self.command.arg2):
            base_command += f"{push_constant_zero_assembly}"

        return base_command

    def get_assembly(self) -> str:
        return self.assembly.format(
            function_name=self.command.arg1,
            nvars=self.command.arg2,
            file_name=self.filename,
            set_local_segment=self._get_setup_of_local_segment()
        )


MOVE_ENDFRAME_BACK = """
    @end_frame
    M=M-1
    A=M
    D=M
"""


class ReturnCommand(BaseFunctionCommand):

    assembly = """
    // return
    
    //
    // Get return address
    //
    @{lcl_address}
    D=M

    @end_frame
    M=D   // stores endFrame = LCL (address where LCL points to)
    
    @5
    D=A
    @end_frame
    D=M-D  // Calculates LCL - 5 (this is the return address of the caller's frame)
    A=D   // Point to the return address of the caller's frame
    D=M   // Store the location of the return address
    @return_address
    M=D   // `return_address` stores the return address for the caller
    
    //
    // Set return value
    //
    {pop_from_stack}
    
    @{arg_address}
    A=M
    M=D  // Stores the top of the stack in ARG (what it will be the top of the stack for the caller
    
    //
    // Reset stack pointer to ARG + 1
    //
    @{arg_address}
    D=M+1
    
    {stack_pointer}
    M=D

    //
    // Recovery of segment addresses
    //
    {move_endframe_back}
    @{that_address}
    M=D
    
    {move_endframe_back}
    @{this_address}
    M=D
    
    {move_endframe_back}
    @{arg_address}
    M=D

    {move_endframe_back}
    @{lcl_address}
    M=D

    //
    // Go back to caller
    //
    @return_address
    A=M
    0;JMP
    """

    def get_assembly(self) -> str:
        return self.assembly.format(
            function_name=self.command.arg1,
            nvars=self.command.arg2,
            file_name=self.filename,
            move_endframe_back=MOVE_ENDFRAME_BACK,
            pop_from_stack=POP_VALUE_ON_TOP_OF_STACK,
            stack_pointer=STACK_POINTER_BASE_ADDRESS,
            lcl_address=SEGMENT_ALIASES[MemorySegment.LOCAL],
            arg_address=SEGMENT_ALIASES[MemorySegment.ARG],
            this_address=SEGMENT_ALIASES[MemorySegment.THIS],
            that_address=SEGMENT_ALIASES[MemorySegment.THAT]
        )
