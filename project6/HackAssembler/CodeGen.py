from Instruction import Instruction
from Instruction import InstructionType
from Instruction import ATypeInstruction
from Instruction import CTypeInstruction

class BinaryCodes:
    OpCode = {
        InstructionType.AType : "0", 
        InstructionType.CType : "1"
    }

    CompCode = {
        "0" : "0101010",
        "1" : "0111111",
        "-1" : "0111010",
        "D" : "0001100",
        "A" : "0110000",
        "!D" : "0001101",
        "!A" : "0110001",
        "-D" : "0001111",
        "-A" : "0110011",
        "D+1" : "0011111",
        "A+1" : "0110111",
        "D-1" : "0001110",
        "A-1" : "0110010",
        "D+A" : "0000010",
        "D-A" : "0010011",
        "A-D" : "0000111",
        "D&A" : "0000000",
        "D|A" : "0010101",
        "M" : "1110000",
        "!M" : "1110001",
        "-M" : "1110011",
        "M+1" : "1110111",
        "M-1" : "1110010",
        "D+M" : "1000010",
        "D-M" : "1010011",
        "M-D" : "1000111",
        "D&M" : "1000000",
        "D|M" : "1010101"
    }

    DestCode = {
        "null" : "000",
        "M" : "001",
        "D" : "010",
        "MD" : "011",
        "A" : "100",
        "AM" : "101",
        "AD" : "110",
        "AMD" : "111"
    }

    JumpCode = {
        "null" : "000",
        "JGT" : "001",
        "JEQ" : "010",
        "JGE" : "011",
        "JLT" : "100",
        "JNE" : "101",
        "JLE" : "110",
        "JMP" : "111"
    }


class CodeGen:
    def __init__(self, parsedInstructionList):
        self.parsedInstructionList = parsedInstructionList

    def generateCode(self):
        for instruction in self.parsedInstructionList:
            if (instruction._instructionType == InstructionType.AType):
                #Handle AType
                value = instruction._ains._value
                ##print(value)
                binaryValue = bin(int(value))
                binaryValue = binaryValue[2:]
                suffix = "0"*(15-len(binaryValue)) + binaryValue
                outBinary = str(BinaryCodes.OpCode[instruction._instructionType]) + suffix

                print(outBinary)
            elif (instruction._instructionType == InstructionType.CType):
                #Handle CType
                comp = instruction._cins._comp
                dest = instruction._cins._dest
                jmp = instruction._cins._jmp

                outBinary = str(BinaryCodes.OpCode[instruction._instructionType]) + "11" + BinaryCodes.CompCode[comp] + BinaryCodes.DestCode[dest] + BinaryCodes.JumpCode[jmp]
                print(outBinary)
            else :
                #Comments or Null Line
                pass