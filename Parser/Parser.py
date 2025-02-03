import sys
from Lexer.TokenKind import * 

class Parser:
    
    def __init__(self, Tokens: list[Token], Meta: dict):
        self.Tokens: list[Token] = Tokens 
        self.Ast: list[dict] = []
        self.Pos: int = 0
        self.Meta: dict = Meta

        self.VarsCalled = self.Meta["VarsCalled"].copy()
        self.Vars = {}

    def Parse(self) -> list[dict]:
        while len(self.Tokens) > self.Pos and self.CToken().Kind != TokenKind.EOF:
            self.Ast.append(self.ParseCToken())
        
        return self.Ast 
    
    def Expect(self, Tk: TokenKind, msg: str):
        tk = self.Adv()
        if tk.Kind != Tk:
            print(f"[{tk.Line}:{tk.Start}:Error] expected {msg} but recived {tk.Value}",file=sys.stderr)
            exit(1)
        else:
            return tk 

    def CToken(self) -> Token:
        return self.Tokens[self.Pos]
    
    def Adv(self) -> Token:
        tk = self.CToken()
        self.Pos+=1
        return tk 
    
    def ParseNum(self) -> dict: 
        Num = self.Adv()

        return {
            "Kind" : "Integer",
            "Value" : Num.Value,
            "Size" : "?",
            "Type" : ["i8", "i16", "i32", "i64"] 
        }
    
    def ParseFloat(self) -> dict:
        Num = self.Adv()

        return {
            "Kind" : "Float",
            "Value" : Num.Value,
            "Size" : "?",
            "Type" : ["f32", "f64"]
        }

    def ParseType(self) -> list[str]: 
        if self.CToken().Kind == TokenKind.Types:
            type_ = self.Adv()
            if type_.Value in ["f32", "f64", "i8", "i16", "i32", "i64"]:
                return [type_.Value,]
        else: 
            tk = self.Adv()
            print(f"[{tk.Line}:{tk.Start}:Error] {tk.Value} is not a valid type", file=sys.stderr)
            exit(1)
    
    def cmptypes(self, Type1, Type2): 
        for i in Type1:
            for i2 in Type2:
                if i2 == i:
                    return True
        return False

    def GetSizeFromType(self, Type):
        return str(int(Type[1:]) // 8)

    def ParseArth(self) -> dict:
        tk = self.Adv()
        
        Type = self.ParseType()
        
        Op1 = self.ParseCToken()
        self.Expect(TokenKind.Comma, "','")
        Op2 = self.ParseCToken()
            
        if self.cmptypes(Op1["Type"], Type) == False or self.cmptypes(Op2["Type"], Type) == False:
            print(f"[{tk.Line}:Error] {Type[0]} does not match with the type of an operand", file=sys.stderr)
            exit(1)
        
        Name = {TokenKind.Add : "Add-Inst", TokenKind.Fadd : "Fadd-Inst"}

        return {
            "Kind" : Name.get(tk.Kind),
            "Op1" : Op1,
            "Op2" : Op2,
            "Size" : self.GetSizeFromType(Type[0]),
            "Type" : Type 
        }

    def ParseVar(self):
        Var = self.Adv()

        if self.CToken().Kind == TokenKind.Equal:
            self.Adv()

            Val = self.ParseCToken()

            self.Vars.update({Var.Value : {"Type" : Val.get("Type"), "Size" : Val.get("Size")}})
            return {
                "Kind" : "Temp_Var",
                "Type" : Val.get("Type"),
                "Size" : Val.get("Size"),
                "Name" : Var.Value,
                "Value" : Val
            }
        
        else:
            if self.VarsCalled[Var.Value] == 1:
                Last = True
            else:
                self.VarsCalled[Var.Value]-=1 
                Last = False 
            
            if Var.Value not in list(self.Vars.keys()):
                print(f"[{Var.Line}:{Var.Start}:Error] {Var.Value} is not a valid vreg", file=sys.stderr)
                exit(1)

            return {
                "Kind" : "Call_Var",
                "Type" : self.Vars[Var.Value]["Type"],
                "Size" : self.Vars[Var.Value]["Size"],
                "Name" : Var.Value,
                "Last" : Last
            }
    
    def LoadVar(self) -> dict:
        Ld = self.Adv()

        Type = self.ParseType()

        self.Expect(TokenKind.Comma, "';'")
        Loading = self.Expect(TokenKind.Variables, "a vreg name")

        self.Expect(TokenKind.Pointarr, "'->'")
        NewName = self.Expect(TokenKind.Variables, "a vreg name")

        self.Vars.update({NewName.Value : {"Type" : Type, "Size" : self.GetSizeFromType(Type[0])}})
        return {
            "Kind" : "Load-inst",
            "Loading" : Loading.Value,
            "Type" : Type,
            "Size" : self.GetSizeFromType(Type[0]),
            "NewName" : NewName.Value
        }

    def ParseRet(self):
        ret = self.Adv()

        Returning = self.ParseCToken()

        return {
            "Kind" : "Ret-inst",
            "Type" : Returning.get("Type"),
            "Size" : Returning.get("Size"),
            "Return" : Returning
        }

    def ParseDef(self):
        deff = self.Adv()
        Name = self.Expect(TokenKind.Functions, " a function name")

        self.Expect(TokenKind.Op_brack, "'('")
        
        Params = []
        while self.CToken().Kind != TokenKind.EOF and self.CToken().Kind != TokenKind.Cl_brack:
            if self.CToken().Kind == TokenKind.EOF:
                print("Eof Error", sys.stderr)
                exit(1)
            elif self.CToken().Kind == TokenKind.Cl_brack:
                break
            else:
                #parse params
                pass 
        

        self.Expect(TokenKind.Cl_brack, "')'")
        self.Expect(TokenKind.Colon, "':'")

        Type = self.ParseType()
        
        self.Expect(TokenKind.Op_c_brack, "'{'")
        Body = []
        while self.CToken().Kind != TokenKind.EOF and self.CToken().Kind != TokenKind.Cl_c_brack:
            if self.CToken().Kind == TokenKind.EOF:
                print("Eof Error", sys.stderr)
                exit(1)
            elif self.CToken().Kind == TokenKind.Cl_c_brack:
                break
            else:
               Body.append(self.ParseCToken())
        
        self.Expect(TokenKind.Cl_c_brack, "'}'")
        return {
            "Kind" : "func-def",
            "Name" : Name.Value,
            "Type" : Type,
            "Size" : "?",
            "Params" : Params,
            "Body" : Body
        }
        

    
    def ParseMeta(self) -> dict: 
        met = self.Adv()

        if met.Value == "?asmcom":
            return {
                "Kind" : "asmcom",
                "Type" : ["?"],
                "Size" : "?",
                "Comment" : self.Adv().Value 
            }
    
 
    def ParseScaleing(self):
        tk = self.Adv()
        Name = {TokenKind.Sext : "Sext-inst", TokenKind.Trunc : "Trunc-inst", TokenKind.Zext : "Zext-inst"}

        Extending = self.Adv()
        self.Expect(TokenKind.To, "'to' token")
        Type = self.ParseType()
        self.Expect(TokenKind.Pointarr, "'->'")
        From = self.ParseType()

        return {
            "Kind" : Name.get(tk.Kind),
            "Type" : Type, 
            "Size" : "?",
            "From" : From,
            "Extending" : Extending.Value
        }
    
    def FloatToInts(self):
        tk = self.Adv()
        
        Name = {TokenKind.Ftui : "Fl-to-uint"}

        From = self.ParseType()
        self.Expect(TokenKind.To, "to keyword")
        To = self.ParseType()
        self.Expect(TokenKind.Comma, "','")

        Ogfloat = self.Adv()
        self.Expect(TokenKind.Pointarr, "'->'")
        NewName = self.Adv()

        return {
            "Kind" : Name.get(tk.Kind),
            "From" : From,
            "Type" : To, 
            "Size" : "?",
            "OgName" : Ogfloat.Value,
            "NewName" : NewName.Value,
        }

    def ParseCToken(self) -> dict:
        CKind = self.CToken().Kind 
        if CKind == TokenKind.Number:
            return self.ParseNum()
        elif CKind == TokenKind.Float:
            return self.ParseFloat()
        elif CKind in [TokenKind.Add, TokenKind.Fadd]:
            return self.ParseArth()
        elif CKind == TokenKind.Variables:
            return self.ParseVar()
        elif CKind == TokenKind.Load:
            return self.LoadVar()
        elif CKind == TokenKind.Ret:
            return self.ParseRet()
        elif CKind == TokenKind.Def:
            return self.ParseDef()
        elif CKind == TokenKind.Meta_Data:
            return self.ParseMeta()
        elif CKind in [TokenKind.Sext, TokenKind.Zext, TokenKind.Trunc]:
            return self.ParseScaleing()
        elif CKind in [TokenKind.Ftui]:
            return self.FloatToInts()
        elif CKind == _: 
            print(f"{self.Adv().Value} <- why is this here", file=sys.stderr)
            exit(1)


