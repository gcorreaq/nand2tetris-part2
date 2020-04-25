import enum


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


class MemorySegment(enum.Enum):
    LOCAL = 'local'
    ARG = 'arg'
    THIS = 'this'
    THAT = 'that'
    TEMP = 'temp'
    STATIC = 'static'
    POINTER = 'pointer'
    CONSTANT = 'constant'
