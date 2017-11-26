class InstructionType:
    NullType = 0
    AType = 1
    CType = 2
    SymbolType = 3
    Undefined = 4

class CTypeInstruction:
    def __init__(self, dest, comp, jmp):
        self._dest = dest
        self._comp = comp
        self._jmp = jmp
    
class ATypeInstruction:
    def __init__(self, value):
        self._value = value

class Instruction:
    def __init__(self, originalCode, instructionType):
        self._instructionType = instructionType 
        self._cins = CTypeInstruction("", "", "")
        self._ains = ATypeInstruction(-1)
        self._originalCode = originalCode
        self._lineNumber = -1
        self._undefinedValue = ""
