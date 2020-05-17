import enum
from itertools import chain


class CommandClass(enum.Enum):
    pass


class ArithmeticCommandClass(CommandClass):
    ADD = 'add'
    SUB = 'sub'
    NEG = 'neg'
    EQ = 'eq'
    GT = 'gt'
    LT = 'lt'
    AND = 'and'
    OR = 'or'
    NOT = 'not'


class StackCommandClass(CommandClass):
    POP = 'pop'
    PUSH = 'push'


class BranchCommandClass(CommandClass):
    LABEL = 'label'
    GOTO = 'goto'
    IF_GOTO = 'if-goto'


class FunctionCommandClass(CommandClass):
    FUNCTION = 'function'
    CALL = 'call'
    RETURN = 'return'


COMMAND_TO_COMMAND_CLASS_MEMBER = {
    member.value: member
    for member in chain(
        ArithmeticCommandClass,
        BranchCommandClass,
        FunctionCommandClass,
        StackCommandClass,
    )
}


class MemorySegment(enum.Enum):
    LOCAL = 'local'
    ARG = 'argument'
    THIS = 'this'
    THAT = 'that'
    TEMP = 'temp'
    STATIC = 'static'
    POINTER = 'pointer'
    CONSTANT = 'constant'
