import re
from Instruction import Instruction
from Instruction import InstructionType
from Instruction import ATypeInstruction
from Instruction import CTypeInstruction

class HackParser:
    def __init__(self, codeList, symbolTable):
        self.codeList = codeList
        self.nextAssignableLineNumber = 0
        self.symbolTable = symbolTable
        self._parsedInstructionList = []
        self.otherAddressBase = 16
    
    def Parse(self):
        ## Parses the entire codeList and returns a list of Instructions
        for code in self.codeList:
            removedComments = self.RemoveComments(code)
            removedWhiteSpace = self.RemoveWhiteSpace(removedComments)
            instructionType = self.ClassifyInstruction(removedWhiteSpace)
            ## print(code.strip() + "   " + str(instructionType))

            instruction = Instruction(removedWhiteSpace, instructionType)
            self.ParseInstruction(instruction)
            self._parsedInstructionList.append(instruction)
        
        self.defineLabelsAndValues()
        ## print(self.symbolTable.symbolValuePair)

 
    def RemoveComments(self, codeStr):
        ## Removes comments from current code string and returns
        string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,codeStr) # remove all occurance streamed comments (/*COMMENT */) from string
        string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all occurance singleline comments (//COMMENT\n ) from string
        return string

    def RemoveWhiteSpace(self, codeStr):
        ## Removes ending newLine, space etc from the current Line
        string = codeStr.strip()
        string.replace(" ", "")
        return string


    def ClassifyInstruction(self, codeStr):
        ## Classifies the current instruction as follows:
        ## 1. A Instruction
        ## 2. C Instruction
        ## 3. Symbol
        ## 4. WhiteSpace - blank lines or commented lines
        if ("@" in codeStr):
            value = codeStr[1:]
            if value.isdigit() :
                return InstructionType.AType
            else:
                return InstructionType.SymbolType
        elif (("=" in codeStr) or (";" in codeStr)):
            return InstructionType.CType
        elif ("(" in codeStr):
            return InstructionType.SymbolType
        else:
            return InstructionType.NullType


    def ParseInstruction(self, instruction):
        ## Takes an instruction and generates the required fields
        ## For A instruction creates the gets the number
        ## For C instruction creates the dest; comp; jmp;
        ## For Symbol creates value in the symbol table
        instructionType = instruction._instructionType
        instructionCode = instruction._originalCode

        if instructionType == InstructionType.AType:
            value = instructionCode[1:]
            valueNumber = int(value)
            newAInstruction = ATypeInstruction(valueNumber)
            instruction._ains = newAInstruction
            instruction._lineNumber = self.nextAssignableLineNumber
            self.nextAssignableLineNumber = self.nextAssignableLineNumber + 1
            
        elif instructionType == InstructionType.CType:
            if ("=" in instructionCode):
                splitInstruction = instructionCode.split("=")
                dest = splitInstruction[0]
                rhsSplit = splitInstruction[1].split(";")
                comp = rhsSplit[0]
                if len(rhsSplit) > 1:
                    jmp = rhsSplit[1]
                else :
                    jmp = "null"
            else :
                splitInstruction = instructionCode.split(";")
                dest = "null"
                comp = splitInstruction[0]
                jmp = splitInstruction[1]
            
            newCInstruction = CTypeInstruction(dest, comp, jmp)
            instruction._cins = newCInstruction
            instruction._lineNumber = self.nextAssignableLineNumber
            self.nextAssignableLineNumber = self.nextAssignableLineNumber + 1

        elif instructionType == InstructionType.SymbolType:
            if ("(" in instructionCode):
                ## Instruction of type ## (LOOP)
                label = instructionCode[1:-1]
                ## Add this label to symbol Table and value as nextInstructionCodeNumber
                self.symbolTable.Add(label, self.nextAssignableLineNumber)
            else :
                ## LabelRef or Variable ## @R0 @LOOP
                variable = instructionCode[1:]
                ## If variable in Symbol Table. Then replace with @value and parse as A-Instruction
                if (self.symbolTable.Contains(variable)) :
                    instruction._instructionType = InstructionType.AType
                    valueNumber = self.symbolTable.GetValue(variable)
                    newAInstruction = ATypeInstruction(valueNumber)
                    instruction._ains = newAInstruction
                    instruction._lineNumber = self.nextAssignableLineNumber
                    self.nextAssignableLineNumber = self.nextAssignableLineNumber + 1

                ## If variable not in Symbol Table - Then we just set this as undefined and to be defined on second pass 
                else :
                    instruction._instructionType = InstructionType.Undefined
                    instruction._undefinedValue = variable
                    instruction._lineNumber = self.nextAssignableLineNumber
                    self.nextAssignableLineNumber = self.nextAssignableLineNumber + 1
        elif instructionType == InstructionType.NullType:
            pass
        else:
            pass

    def defineLabelsAndValues(self):
        for instruction in self._parsedInstructionList:
            if instruction._instructionType == InstructionType.Undefined :
                # If the value for this symbol is there => LabelRef / Already variableName has been given the value
                if (self.symbolTable.Contains(instruction._undefinedValue)):
                    instruction._instructionType = InstructionType.AType
                    instruction._ains._value = self.symbolTable.GetValue(instruction._undefinedValue)
                # If the value for this symbol isn't there => Label
                else :
                    instruction._instructionType = InstructionType.AType
                    instruction._ains._value = self.otherAddressBase
                    self.symbolTable.Add(instruction._undefinedValue, instruction._ains._value)
                    self.otherAddressBase = self.otherAddressBase + 1

