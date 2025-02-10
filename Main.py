import sys
import json
from Parser.Parser import *
from Lexer.Lexer import *
from CodeGen.CodeGen import *
from Update import *
import os
import subprocess

#Info-------
ZircVer: str = "0.03"
#------------

def main(argc: int = sys.argv.__len__(), argv: list[str] = sys.argv):

    File = argv[1:2]

    if File == []:
        print("zirc: no input files", file=sys.stderr)
        sys.exit(1)
    
    if File[0] == "--h":
        print("Usage: zirc <file> [options]")

        print("options:")
        print("     -o <file>            puts the output into <file>")
        print("     -filet=<filetype>    generates an asm file(-filet=asm) an obj file(-filet=o)")
        print("     --dwarf              enables dwarf")
        print("     -link=<file>         adds a libary to links with")
        print("     --debug              adds dwarf debugging support")
        sys.exit(0)

    elif File[0] == "--v":
        print(ZircVer)        
        sys.exit(0)
    
    elif File[0] == "--update":
        Update(ZircVer)
    
    else:
        Name: str = ""
        Flags: list[str] = []
        if File[0][-2:] != "zr":
            print(f"Unknown flag '{File[0]}'", file=sys.stderr)
        else:
            try:
                with open(File[0], "r") as Code:
                    SourceCode: str = Code.read()
            except FileNotFoundError:
                print(f"zirc: no such file or directory '{File[0]}'", file=sys.stderr)
            else:
                if "--name" in argv:
                    Name: str = argv[argv.index("--name") + 1] 
                if "--debug" in argv:
                    Flags.append("debug")

                LexerClass: Lexer = Lexer(SourceCode)
                LexedTokens: list[Token] = LexerClass.Lex()

                if "-lexdbg" in argv:
                    for i in LexedTokens: print(i)

                ParserClass: Parser = Parser(LexedTokens, LexerClass.Meta)
                Ast: list[dict] = ParserClass.Parse()

                if "-parsedbg" in argv:
                    print(json.dumps(Ast, indent=4))
                
                CodeGenclass: CodeGen = CodeGen(Ast, Flags, {
                    "Dir" : os.getcwd(),
                    "ProvFile" : File[0],
                    "File" : os.path.basename(File[0])
                })

                AsmCode: str = CodeGenclass.Gen()

                with open(f"{Name}.s", "w") as Fileasm:
                    Fileasm.write(AsmCode)

if __name__ == '__main__':
    main()
    sys.exit(0)

