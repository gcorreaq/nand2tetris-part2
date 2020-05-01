from io import StringIO

import pytest

from enumerations import (
    ArithmeticCommandClass,
    MemorySegment,
    StackCommandClass,
)
from assembly_commands import (
    COMPARISON_COMMAND_TO_OPERATOR,
    DOUBLE_ARG_ARITHMETIC_COMMAND_TO_OPERATOR,
    SINGLE_ARG_ARITHMETIC_COMMAND_TO_OPERATOR,
)


@pytest.fixture
def file_with_comments():
    initial_value = '// This is a test\n// And nothing is here'
    return StringIO(initial_value=initial_value)


@pytest.fixture
def file_with_empty_lines():
    initial_value = '\n    \n\t\n'
    return StringIO(initial_value=initial_value)


@pytest.fixture(params=ArithmeticCommandClass)
def file_with_arithmetic_command(request):
    dummy_file_obj = StringIO(
        initial_value=f"{request.param.value}"
    )
    return dummy_file_obj, request.param


ALL_STACK_COMMANDS_AND_MEMORY_SEGMENTS = [
    (stack_command, memory_segment)
    for stack_command in StackCommandClass
    for memory_segment in MemorySegment
]


@pytest.fixture(params=ALL_STACK_COMMANDS_AND_MEMORY_SEGMENTS)
def file_with_stack_command(request):
    stack_command, memory_segment = request.param
    dummy_file_obj = StringIO(
        initial_value=f"{stack_command.value} {memory_segment.value} 0"
    )
    return dummy_file_obj, stack_command, memory_segment


@pytest.fixture
def file_with_garbage():
    return StringIO(
        initial_value='this is nothing like a command'
    )


@pytest.fixture(params=COMPARISON_COMMAND_TO_OPERATOR.items())
def comparison_command(request):
    command_name, expected_operator = request.param
    return command_name, expected_operator


@pytest.fixture(params=SINGLE_ARG_ARITHMETIC_COMMAND_TO_OPERATOR.items())
def one_argument_arithmetic_command(request):
    command_name, expected_operator = request.param
    return command_name, expected_operator


@pytest.fixture(params=DOUBLE_ARG_ARITHMETIC_COMMAND_TO_OPERATOR.items())
def two_argument_arithmetic_command(request):
    command_name, expected_operator = request.param
    return command_name, expected_operator
