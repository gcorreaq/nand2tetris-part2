import pytest

from command import Command
from command_writer import (
    DOUBLE_ARG_ARITHMETIC_COMMAND_TO_OPERATOR,
    TwoArgumentArithmeticCommand,
)


@pytest.fixture(params=DOUBLE_ARG_ARITHMETIC_COMMAND_TO_OPERATOR.items())
def two_argument_arithmetic_command(request):
    command_name, expected_operator = request.param
    return command_name, expected_operator


def test_includes_original_operator_in_comment(two_argument_arithmetic_command):
    command_name, expected_operator = two_argument_arithmetic_command
    command_obj = Command(command_name)

    assembly = TwoArgumentArithmeticCommand(command_obj).get_assembly()

    assert f"// {command_name}" in assembly


def test_returns_expected_operation(two_argument_arithmetic_command):
    command_name, expected_operator = two_argument_arithmetic_command
    command_obj = Command(command_name)

    assembly = TwoArgumentArithmeticCommand(command_obj).get_assembly()

    assert f"D=D{expected_operator}M" in assembly
