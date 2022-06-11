import enum

class Hierarchy(enum.IntEnum):
    MULT_DIV = 1
    SUM_SUB = 2
    COMPARE = 3
    LOGIC = 4
    PAREN = 5
    ASSIGN = 6
    RETURN = 7
    OUTPUT = 8
    INPUT = 9
    GOTOF = 10
    GOTO = 11
    GOTOW = 12
    END_FUNC = 13
    ERA = 14
    PARAMS = 15
    GOSUB = 16
    ASSIGN_R = 17
    VER = 18
    ARR_BASE = 19
    ARR_SD = 20
    ARR_SDS = 21
    END = 22

class OpID():
    IDOperators = {
        "*": 1,
        "/": 2,
        "+": 3,
        "-": 4,
        "<": 5,
        "<=": 6,
        ">": 7,
        ">=": 8,
        "==": 9,
        "!=": 10,
        "&&": 11,
        "||": 12,
        "=": 13,
        "return": 14,
        "input": 15,
        "output": 16,
        "gotof" : 17,
        "goto": 18,
        "endfunc" : 19,
        "era" : 20,
        "params" : 21,
        "gosub" : 22,
        "assignr" : 23,
        "ver" : 24,
        "arrbase" : 25,
        "arrsd" : 26,
        "arrsds" : 27,
        "end" : 28
    }

    def getOpID(self, op: str) -> int:
        return self.IDOperators[op]

    def getOpIDKey(self, value: int) -> str:
        ans = [k for k, v in self.IDOperators.items() if v == value]
        return ans

class Operators():
    HierarchyOp = {
        "(": Hierarchy.PAREN,
        ")": Hierarchy.PAREN,
        "*": Hierarchy.MULT_DIV,
        "/": Hierarchy.MULT_DIV,
        "+": Hierarchy.SUM_SUB,
        "-": Hierarchy.SUM_SUB,
        '<': Hierarchy.COMPARE,
        '<=':Hierarchy.COMPARE,
        '>': Hierarchy.COMPARE,
        '>=' : Hierarchy.COMPARE,
        '==' : Hierarchy.COMPARE,
        '!=' : Hierarchy.COMPARE,
        '&&': Hierarchy.LOGIC,
        '||': Hierarchy.LOGIC,
        "=": Hierarchy.ASSIGN,
        "return": Hierarchy.RETURN,
        "input": Hierarchy.INPUT,
        "output": Hierarchy.OUTPUT,
        "gotof": Hierarchy.GOTOF,
        "goto": Hierarchy.GOTO,
        "gotow": Hierarchy.GOTOW,
        "endfunc": Hierarchy.END_FUNC,
        "era" : Hierarchy.ERA,
        "params" : Hierarchy.PARAMS,
        "gosub" : Hierarchy.GOSUB,
        "assignr" : Hierarchy.ASSIGN_R,
        "ver" : Hierarchy.VER,
        "addbase" : Hierarchy.ARR_BASE,
        "s1d2" : Hierarchy.ARR_SD,
        "s1d2s2" : Hierarchy.ARR_SDS,
        "end" : Hierarchy.END
    }