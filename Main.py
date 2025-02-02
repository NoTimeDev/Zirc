import sys
import json
from Lexer.Lexer import *
from Parser.Parser import *

from CodeGen.CodeGen import * 
with open(sys.argv[1], "r") as File:
    Code = ""   
    
    for i in File.readlines():
        Code+=i+" "

LexerClass: Lexer = Lexer(Code)
Tokens: list[Token] = LexerClass.Lex()


#for i in Tokens: print(i)

ParserClass: Parser = Parser(Tokens, LexerClass.Meta)
Ast: list[dict] = ParserClass.Parse()

# print(json.dumps(Ast, indent=4))

CodeGenClass: CodeGen = CodeGen(Ast)
AsmCode = CodeGenClass.GenAsm()


with open("Out.asm", "w") as File:
    File.write(AsmCode)
