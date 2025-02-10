from enum import Enum, auto 

class TokenKind(Enum):
    #Macs
    private = auto()
    public = auto()
    cdelc = auto()
    stdcall = auto()
    
    #debug 
    CompilationUnit = auto()
    File = auto()
    Func = auto()
    Mark = auto()

    #instructions
    Add = auto()
    
    Fadd = auto()

    Ret = auto()
    Def = auto()
    Load = auto()
    To = auto()
    Sext = auto()
    Zext = auto()
    Trunc = auto()
    
    Ftui = auto()
    Ftsi = auto()

    Uitf = auto()
    Sitf = auto()

    Ftrunc = auto()
    Fext = auto()

    #variables
    Meta_Data = auto()
    Variables = auto()
    Functions = auto()

    #Constants
    Strings = auto()
    Number = auto()
    Float = auto()

    #Types
    Types = auto()

    #Symbols
    Colon = auto()
    Equal = auto()
    Comma = auto()

    Op_brack = auto()
    Cl_brack = auto()
    
    Op_c_brack = auto()
    Cl_c_brack = auto()
    
    EOF = auto()
    
    Pointarr = auto()

class Token:
    def __init__(self, kind: TokenKind, Line: int, Start: int, Value: str):
        self.Line: int = Line 
        self.Start: int = Start 
        self.Value: str = Value
        self.Kind: TokenKind = kind 

    def __repr__(self) -> str:
        return "{" +f'"Kind" : {self.Kind}, "Line" : {self.Line}, "Start" : {self.Start}, "Value" : \"{self.Value}\"' + "}"
