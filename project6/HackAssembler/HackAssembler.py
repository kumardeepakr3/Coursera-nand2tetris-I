from HackParser import HackParser
from Instruction import InstructionType
from SymbolTable import SymbolTable
from CodeGen import CodeGen

inputFile = "/mnt/c/Users/deku.FAREAST/Documents/nand2tetris/projects/06/rect/Rect.asm"

if __name__ == "__main__":
    file = open(inputFile, 'r')
    codeList = file.readlines()

    ## codeList = ["@200 //CommentedCode \n", "AD=D+1;JEQ"]
    symbolTable = SymbolTable()
    myParser = HackParser(codeList, symbolTable)
    myParser.Parse()
    parsedInstructionList = myParser._parsedInstructionList
    myCodeGenerator = CodeGen(parsedInstructionList)
    myCodeGenerator.generateCode()
