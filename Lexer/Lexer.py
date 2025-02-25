import sys

from .TokenKind import *


class Lexer:
    def __init__(self, Code: str):
        self.Code: str = Code
        self.Meta: dict = {"Funcs" : [], "Vars" : [], "Labels" : [], "VarsCalled" : {}}
    
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
            
            elif cchar == '-' and self.Code[Pos + 1] == ">":
                Add(Coloum, Line, TokenKind.Pointarr, "->")
                Pos+=2; Coloum+=2
            elif cchar == "-" and self.Code[Pos + 1].isdigit():
                Start: int = Coloum
                Var: str = "-"
                Pos+=1; Coloum+=1 
                while self.Code[Pos].isdigit() or self.Code[Pos] == ".":
                        Var+=self.Code[Pos]
                        Pos+=1; Coloum+=1 
                    
                if Var.count(".") == 1:
                    Add(Start, Line, TokenKind.Float, Var)
                else:
                    Add(Start, Line, TokenKind.Number, Var)


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
                if cchar.isalpha() or cchar == "_":
                    Start: int = Coloum
                    String: str = ""
                    while self.Code[Pos].isalnum() or self.Code[Pos] == "_":
                        String+=self.Code[Pos]
                        Pos+=1; Coloum+=1

                    Ap: dict[str, TokenKind] = {
                        "add" : TokenKind.Add,
                        "fadd" : TokenKind.Fadd,

                        "ret" : TokenKind.Ret,
                        "def" : TokenKind.Def,
                        "load" : TokenKind.Load,
                        "to" : TokenKind.To,
                        
                        "fext" : TokenKind.Fext,
                        "sext" : TokenKind.Sext,
                        "zext" : TokenKind.Zext, 
                        
                        "ftrunc" : TokenKind.Ftrunc,
                        "trunc" : TokenKind.Trunc,

                        "uitf" : TokenKind.Uitf,
                        "sitf" : TokenKind.Sitf,
                        
                        "ftui" : TokenKind.Ftui, 
                        "ftsi" : TokenKind.Ftsi,
                        
                        "__private" : TokenKind.private,
                        "__public" : TokenKind.public,
                        "__stdcall" : TokenKind.stdcall,
                        "__cdelc" : TokenKind.cdelc,
                        
                        "file" : TokenKind.File,
                        "func" : TokenKind.Func,
                        "compunit" : TokenKind.CompilationUnit,
                        "mark" : TokenKind.Mark,

                        "i8" : TokenKind.Types,
                        "i16" : TokenKind.Types,
                        "i32" : TokenKind.Types,
                        "i64" : TokenKind.Types,

                        "f32" : TokenKind.Types,
                        "f64" : TokenKind.Types,
                    }

                    if String not in list(Ap.keys()):
                        print(f"{Line}:{Start} {String} is not a valid instruction",file=sys.stderr)
                        sys.exit(1)
                    
                    Add(Start, Line, Ap[String], String)
                elif cchar == "$":
                    Start: int = Coloum
                    Var: str = ""
                    while self.Code[Pos] != " " and self.Code[Pos] != "\n":
                        Var+=self.Code[Pos]
                        Pos+=1; Coloum+=1 
                    Add(Start, Line, TokenKind.Variables, Var)
                    self.Meta["Vars"].append(Var)
                    if self.Meta["VarsCalled"].get(Var) == None:
                        self.Meta["VarsCalled"].update({Var : 0})
                    else:
                        self.Meta["VarsCalled"][Var]+=1 
                elif cchar == "@":
                    Start: int = Coloum
                    Var: str = "@"
                    Pos+=1 
                    Coloum+=1
                    while self.Code[Pos].isalnum() or self.Code[Pos] == "_":
                        Var+=self.Code[Pos]
                        Pos+=1; Coloum+=1 
                    Add(Start, Line, TokenKind.Functions, Var)
                    self.Meta["Funcs"].append(Var)

                elif cchar == "?":
                    Start: int = Coloum
                    Var: str = ""
                    while self.Code[Pos] != " " and self.Code[Pos] != "\n":
                        Var+=self.Code[Pos]
                        Pos+=1; Coloum+=1 

                    Add(Start, Line, TokenKind.Meta_Data, Var)
                elif cchar.isdigit() or cchar.lower() == "x" and self.Code[Pos + 1:Pos + 2].isdigit():
                    Start: int = Coloum
                    Var: str = ""
                    while self.Code[Pos].isdigit() or self.Code[Pos] in "ABCDEF.abcdefxX":
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
                     print(f"[{Line}:{Coloum}:Error] \"{cchar}\" is not a valid token", file=sys.stderr)
                
        Add(0, 0, TokenKind.EOF, "end of file")                
        return Tokens
                                                                 
