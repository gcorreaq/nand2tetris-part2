from io import StringIO

import pytest

from parser import (
    ArithmeticCommandClass,
    Command,
    Parser,
    StackCommandClass
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


def test_discards_comments(file_with_comments):
    parser = Parser(file_with_comments)

    parsed_commands = list(parser.parse_file())

    assert len(parsed_commands) == 0


def test_discard_blank_lines(file_with_empty_lines):
    parser = Parser(file_with_empty_lines)

    parsed_commands = list(parser.parse_file())

    assert len(parsed_commands) == 0


def test_parses_arithmetic_commands(file_with_arithmetic_command):
    file_obj, expected_command_class = file_with_arithmetic_command
    parser = Parser(file_obj)

    parsed_commands = list(parser.parse_file())

    assert len(parsed_commands) == 1
    command = parsed_commands[0]
    assert command.command_class == expected_command_class
    assert command.target_segment is None
    assert command.index is None


def test_parses_stack_commands(file_with_stack_command):
    file_obj, expected_command_class = file_with_stack_command
    parser = Parser(file_obj)

    parsed_commands = list(parser.parse_file())

    assert len(parsed_commands) == 1
    command = parsed_commands[0]
    assert command.command_class == expected_command_class
    assert command.target_segment == 'segment'
    assert command.index == 0


def test_raises_exception_with_unknown_command(file_with_garbage):
    parser = Parser(file_with_garbage)

    with pytest.raises(ValueError) as exception_info:
        list(parser.parse_file())

    assert 'Unrecognized command' in str(exception_info.value)
