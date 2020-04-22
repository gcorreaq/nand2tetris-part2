from io import StringIO

import pytest

from command import ArithmeticCommandClass, StackCommandClass


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


@pytest.fixture(params=StackCommandClass)
def file_with_stack_command(request):
    dummy_file_obj = StringIO(
        initial_value=f"{request.param.value} segment 0"
    )
    return dummy_file_obj, request.param


@pytest.fixture
def file_with_garbage():
    return StringIO(
        initial_value='this is nothing like a command'
    )