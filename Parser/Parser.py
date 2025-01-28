import sys
from Lexer.TokenKind import *

class Parser:
    def __init__(self, Tokens: list[Token]):
        self.Tokens: list[Token] = Tokens
        self.Pos: int = 0

        self.VarsTypes: dict = {}
    
        self.Ast = {
            "Body" : []
        }
    def CToken(self) -> Token:
        return self.Tokens[self.Pos]

    def Adv(self) -> Token:
        tk = self.CToken()
        if tk.Kind == TokenKind.EOF:
            print("Error: Eof Error")
            exit(1)
        self.Pos+=1
        return tk 
    
    
    def Expect(self, Kind: TokenKind, Val: str) -> Token:
        if self.CToken().Kind != Kind:
            print(f"Error:{self.CToken().Line}:{self.CToken().Start}: Expected {Val} but found {self.CToken().Value}", file=sys.stderr)
            exit(1)
        else:
            return self.Adv()

    def GetAst(self):
        while len(self.Tokens) > self.Pos:
            if self.CToken().Kind == TokenKind.EOF:
                break 
            self.Ast['Body'].append(self.Parse())
        
        return self.Ast

    def Parse(self): 
        match(self.CToken().Kind):
            case TokenKind.Variables:
                Node = self.ParseVars()
            case TokenKind.Def:
                Node = self.ParseFunc()
            case TokenKind.Add:
                Node = self.ParseAdd()
            case TokenKind.Number:
                Node = self.ParseInt()
            case TokenKind.Load:
                Node = self.ParseLoad()
            case TokenKind.Ret:
                Node = self.ParseRet()
            case _:
                print(f"not added {self.CToken().Kind}")
                exit(1)
        return Node
    
    def ParseRet(self):
        self.Adv()
        Node = self.Parse()
        return {
            "Kind" : "ret inst",
            "Type" : Node.get('Type'),
            "ReturnVal" : Node
        }

    def ParseLoad(self):
        self.Adv()
        Type = self.ParseType()
        self.Expect(TokenKind.Comma, ',')

        ToLoad = self.Adv()
        New =  self.Expect(TokenKind.Variables, "a var name").Value 
        self.VarsTypes.update({New : Type})

        return {
            "Kind" : "Load inst",
            "Type" : Type,
            "Loading" : ToLoad.Value,
            "NewName" : New
        }
    def cmptypes(self, t1, t2):
        if t1 == "int" and t2 in ["i64", "i32", "i16", "i8", "i1"]:
            return True
        elif t2 == "int" and t1 in ["i64", "i32", "i16", "i8", "i1"]:
            return True 
        else:
            return t1 == t2 

    def ParseAdd(self):
        e = self.Adv()
        
        Type = self.ParseType()
        Op1 = self.Parse()
        self.Expect(TokenKind.Comma, ",")
        Op2 = self.Parse()
        
        if self.cmptypes(Type.get("Type"), Op1.get("Type").get("Type")) == False or self.cmptypes(Type.get("Type"), Op2.get("Type").get("Type")) == False:
            print(f"Error:{e.Line}: {Type.get("Type")} does not match with an operand",file=sys.stderr)
            exit(1)

        return {
            "Kind" : "Add inst",
            "Type" : Type,
            "Op1" : Op1,
            "Op2" : Op2 
        }

    def ParseInt(self):
        Int = self.Adv()

        return {
            "Kind" : "Integer",
            "Value" : Int.Value,
            "Type" : {"Type" : "int"}
        }

    def ParseType(self):
        if self.CToken().Kind == TokenKind.Types:
            return {
                "Type" : self.Adv().Value,
            }

        else:
            self.Expect(TokenKind.Types, "a type")
    def ParseFunc(self):
        self.Adv()

        Name = self.Expect(TokenKind.Functions, "a function name")
        self.Expect(TokenKind.Op_brack, "(")
        
        Types = []
        while self.CToken().Kind != TokenKind.Cl_brack:
            if self.CToken().Kind == TokenKind.Cl_brack:
                break 
            Types.append(self.ParseType())
        self.Expect(TokenKind.Cl_brack, ")")

        self.Expect(TokenKind.Colon, ":")
        
        RetType = self.ParseType()

        self.Expect(TokenKind.Op_c_brack, "{")
        Body = []
        while self.CToken().Kind != TokenKind.Cl_c_brack:
            if self.CToken().Kind == TokenKind.Cl_brack:
                break 
            Body.append(self.Parse())
        self.Expect(TokenKind.Cl_c_brack, "}")
        
        return {
            "Kind" : "Function",
            "Name" : Name.Value,
            "RetType" : RetType,
            "Arguments" : Types,
            "Body" : Body,
            "Type" : {"Type" : "Null"},
        }
    def ParseVars(self):
        tk = self.Adv()
         
        if self.CToken().Kind == TokenKind.Equal:
            self.Adv()

            Node = self.Parse()
            

            self.VarsTypes.update({tk.Value : Node.get("Type").get("Type")})
            return {
                "Kind" : "TempVariable",
                "Type" : Node.get("Type"),
                "Value" : Node,
                "Name" : tk.Value,
            }
        else:
            return {
                "Kind" : "CallTempVar",
                "Type" : self.VarsTypes.get(tk.Value),
                "Name" : tk.Value
            }
