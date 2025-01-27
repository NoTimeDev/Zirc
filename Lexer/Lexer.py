import sys
from .TokenKind import *


class Lexer:
    def __init__(self, Code: str):
        self.Code: str = Code
        self.FunctionList: list[str] = []

    def Lex(self):
        Tokens: list[Token] = []

        Pos: int = 0
        Coloum: int = 1
        Line: int = 1

        def Add(Start: int, Line: int, Kind: TokenKind, Val: str):
            Tokens.append(Token(Kind, Line, Start, Val))

        while Pos < len(self.Code):
            cchar = self.Code[Pos]

            if cchar in [' ', '\t']:
                Pos+=1
                Coloum+=1

            elif cchar ==  "\n":
                Line+=1
                Pos+=1
                Coloum = 1

            elif cchar == '#':
                while self.Code[Pos] != "\n":
                    Pos+=1
                    Coloum+=1
                Pos+=1
                Coloum+=1

            elif cchar == ":":
                Add(Coloum, Line, TokenKind.Colon, ":")
                Pos+=1; Coloum+=1
            elif cchar == "{":
                Add(Coloum, Line, TokenKind.Op_c_brack, "{")
                Pos+=1; Coloum+=1
            
            elif cchar == "}":
                Add(Coloum, Line, TokenKind.Cl_c_brack, "}")
                Pos+=1; Coloum+=1

            elif cchar == "(":
                Add(Coloum, Line, TokenKind.Op_brack, "(")
                Pos+=1; Coloum+=1

            elif cchar == ")":
                Add(Coloum, Line, TokenKind.Cl_brack, ")")
                Pos+=1; Coloum+=1

            elif cchar == "=":
                Add(Coloum, Line, TokenKind.Equal, "=")
                Pos+=1; Coloum+=1

            elif cchar == ",":
                Add(Coloum, Line, TokenKind.Comma, ",")
                Pos+=1; Coloum+=1
            
            else:
                if cchar.isalpha():
                    Start: int = Coloum
                    String: str = ""
                    while self.Code[Pos].isalnum():
                        String+=self.Code[Pos]
                        Pos+=1; Coloum+=1

                    Ap: dict[str, TokenKind] = {
                        "add" : TokenKind.Add,
                        "ret" : TokenKind.Ret,
                        "def" : TokenKind.Def,
                        "load" : TokenKind.Load,

                        "i1" : TokenKind.Types,
                        "i8" : TokenKind.Types,
                        "i16" : TokenKind.Types,
                        "i32" : TokenKind.Types,
                        "i64" : TokenKind.Types,
                    }
                    if String not in list(Ap.keys()):
                        print(f"{Line}:{Start} {String} is not a valid instruction",file=sys.stderr)
                        exit(1)
                    
                    Add(Start, Line, Ap[String], String)
                elif cchar == "$":
                    Start: int = Coloum
                    Var: str = ""
                    while self.Code[Pos] != " " and self.Code[Pos] != "\n":
                        Var+=self.Code[Pos]
                        Pos+=1; Coloum+=1 
                    Add(Start, Line, TokenKind.Variables, Var)
                elif cchar == "@":
                    Start: int = Coloum
                    Var: str = "@"
                    Pos+=1 
                    Coloum+=1
                    while self.Code[Pos].isalnum() or self.Code[Pos] == "_":
                        Var+=self.Code[Pos]
                        Pos+=1; Coloum+=1 
                    Add(Start, Line, TokenKind.Functions, Var)
                    self.FunctionList.append(Var)
                elif cchar == "?":
                    Start: int = Coloum
                    Var: str = ""
                    while self.Code[Pos] != " " and self.Code[Pos] != "\n":
                        Var+=self.Code[Pos]
                        Pos+=1; Coloum+=1 

                    Add(Start, Line, TokenKind.Meta_Data, Var)
                elif cchar.isdigit():
                    Start: int = Coloum
                    Var: str = ""
                    while self.Code[Pos].isdigit() or self.Code[Pos] == ".":
                        Var+=self.Code[Pos]
                        Pos+=1; Coloum+=1 
                    
                    if Var.count(".") == 1:
                        Add(Start, Line, TokenKind.Float, Var)
                    else:
                        Add(Start, Line, TokenKind.Number, Var)

                elif cchar == '"':
                    Start: int = Coloum
                    Var: str = ""
                    Pos+=1; Coloum+=1 
                    while self.Code[Pos] != '"':
                        Var+=self.Code[Pos]
                        Pos+=1; Coloum+=1 

                    Pos+=1; Coloum+=1 
                    Add(Start, Line, TokenKind.Strings, Var)
                else:
                    print(f"{Line}:{Coloum} \"{cchar}\" is not a valid token", file=sys.stderr)
                
        Add(0, 0, TokenKind.EOF, "end of file")                
        return Tokens
                                                
