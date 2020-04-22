import pytest

from parser import (
    Parser
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
