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

ParserClass: Parser = Parser(Tokens)
Ast: dict = ParserClass.GetAst() 
#print(json.dumps(Ast, indent=4))

CodeGenClass: CodeGen = CodeGen(Ast)
Asm: str = CodeGenClass.GetAsm()

with open(sys.argv[2], "w") as File:
    File.write(Asm)
