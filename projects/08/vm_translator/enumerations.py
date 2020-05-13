import enum
from itertools import chain


class ArithmeticCommandClass(enum.Enum):
    ADD = 'add'
    SUB = 'sub'
    NEG = 'neg'
    EQ = 'eq'
    GT = 'gt'
    LT = 'lt'
    AND = 'and'
    OR = 'or'
    NOT = 'not'


class StackCommandClass(enum.Enum):
    POP = 'pop'
    PUSH = 'push'


COMMAND_TO_COMMAND_CLASS_MEMBER = {
    member.value: member
    for member in chain(
        ArithmeticCommandClass,
        BranchCommandClass,
        StackCommandClass
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
