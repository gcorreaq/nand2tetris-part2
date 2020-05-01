from command import Command
from assembly_commands import (
    ComparisonCommand,
    OneArgumentArithmeticCommand,
    TwoArgumentArithmeticCommand,
)


def test_returns_expected_operation_for_comparison_operator(comparison_command):
    command_name, expected_operator = comparison_command
    command_obj = Command(command_name)

    assembly = ComparisonCommand(command_obj).get_assembly()

    assert f"D;{expected_operator}" in assembly


def test_returns_expected_operation_for_single_operator(one_argument_arithmetic_command):
    command_name, expected_operator = one_argument_arithmetic_command
    command_obj = Command(command_name)

    assembly = OneArgumentArithmeticCommand(command_obj).get_assembly()

    assert f"D={expected_operator}M" in assembly


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
