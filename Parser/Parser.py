from re import I
import sys
from Lexer.TokenKind import * 
import os


class Parser:
    
    def __init__(self, Tokens: list[Token], Meta: dict):
        self.Tokens: list[Token] = Tokens 
        self.Ast: list[dict] = []
        self.Pos: int = 0
        self.Meta: dict = Meta

        self.VarsCalled = self.Meta["VarsCalled"].copy()

        self.Debug = self.Meta
        self.Vars = {}
        
        self.marks = {}
    def Parse(self) -> list[dict]:
        while len(self.Tokens) > self.Pos and self.CToken().Kind != TokenKind.EOF:
            self.Ast.append(self.ParseCToken())
        
        return self.Ast 
    
    def Expect(self, Tk: TokenKind, msg: str):
        tk = self.Adv()
        if tk.Kind != Tk:
            print(f"[{tk.Line}:{tk.Start}:Error] expected {msg} but recived {tk.Value}",file=sys.stderr)
            sys.exit(1)
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
            sys.exit(1)
    
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
            sys.exit(1)
        
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
                sys.exit(1)

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
                sys.exit(1)
            elif self.CToken().Kind == TokenKind.Cl_brack:
                break
            else:
                #parse params
                pass 
        

        self.Expect(TokenKind.Cl_brack, "')'")
        self.Expect(TokenKind.Colon, "':'")

        Type = self.ParseType()
        Mods = []
        while self.CToken().Kind != TokenKind.EOF and self.CToken().Kind != TokenKind.Op_c_brack:
            if self.CToken().Kind == TokenKind.EOF:
                print("Eof Error", sys.stderr)
                sys.exit(1)
            elif self.CToken().Kind == TokenKind.Op_c_brack:
                break
            else:
               Mods.append(self.Adv().Value)
            
        self.Expect(TokenKind.Op_c_brack, "'{'")
        Body = []
        while self.CToken().Kind != TokenKind.EOF and self.CToken().Kind != TokenKind.Cl_c_brack:
            if self.CToken().Kind == TokenKind.EOF:
                print("Eof Error", sys.stderr)
                sys.exit(1)
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
            "Modifiers": Mods,
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
        elif met.Value == "?.debug":
            debugging = self.Adv()

            if debugging.Kind == TokenKind.CompilationUnit:
                self.Expect(TokenKind.Op_c_brack, "{")  
                
                Compinfo = {"Producer" : "Zirc V1-0, Zed-intermidiate-represention-code", "Lang" : 90}
                
                while self.CToken().Kind != TokenKind.EOF and self.CToken().Kind != TokenKind.Cl_c_brack:
                    if self.CToken().Kind == TokenKind.EOF:
                        print("Eof Error", sys.stderr)
                        sys.exit(1)
                    elif self.CToken().Kind == TokenKind.Cl_c_brack:
                        break
                    else:
                        Item = self.Expect(TokenKind.Strings, "a string")
                        
                        if Item.Value == "Producer":
                            self.Expect(TokenKind.Colon, ":")
                            prodinfo = self.Expect(TokenKind.Strings, " a string")
                            self.Expect(TokenKind.Comma, ",")
                            Compinfo["Producer"] = prodinfo.Value
                        elif Item.Value == "Lang":
                            self.Expect(TokenKind.Colon, ":")
                            langinfo = self.Expect(TokenKind.Number, "a number")
                            self.Expect(TokenKind.Comma, ",")
                            Compinfo["Lang"] = int(langinfo.Value)
                        else:
                            print(f"[{Item.Line}:{Item.Start}:Error] '{Item.Value}' is not apart of the compuint metadata")

                self.Expect(TokenKind.Cl_c_brack, "'}'")
                

                return {
                    "Kind" : "CompilationUnit_debug",
                    "Size" : "?",
                    "Type" : ["?"],
                    "Info" : Compinfo,
                }
            elif debugging.Kind == TokenKind.Func:
                self.Expect(TokenKind.Op_c_brack, "{")  
                
                funcinfo = {"external" : 1, "symbol" : "", "name" : "unknown func name", "external" : 1, "type" : "", "void" : "False", "params" : "False", "ret" : "", "file" : 1, "line" : 0, "col" : 0}

                
                while self.CToken().Kind != TokenKind.EOF and self.CToken().Kind != TokenKind.Cl_c_brack:
                    if self.CToken().Kind == TokenKind.EOF:
                        print("Eof Error", sys.stderr)
                        sys.exit(1)
                    elif self.CToken().Kind == TokenKind.Cl_c_brack:
                        break
                    else:
                        Item = self.Expect(TokenKind.Strings, "a string")
                        
                        if Item.Value == "symbol":
                            self.Expect(TokenKind.Colon, ":")
                            prodinfo = self.Expect(TokenKind.Strings, " a string")
                            self.Expect(TokenKind.Comma, ",")
                            funcinfo["symbol"] = prodinfo.Value       
                        elif Item.Value == "name":
                            self.Expect(TokenKind.Colon, ":")
                            langinfo = self.Expect(TokenKind.Strings, "a string")
                            self.Expect(TokenKind.Comma, ",")
                            funcinfo["name"] = langinfo.Value
                        elif Item.Value == "file":
                            self.Expect(TokenKind.Colon, ":")
                            langinfo = self.Expect(TokenKind.Number, "a number")
                            self.Expect(TokenKind.Comma, ",")
                            funcinfo["file"] = int(langinfo.Value) 
                        elif Item.Value == "line":
                            self.Expect(TokenKind.Colon, ":")
                            langinfo = self.Expect(TokenKind.Number, "a number")
                            self.Expect(TokenKind.Comma, ",")
                            funcinfo["line"] = int(langinfo.Value)   
                        elif Item.Value == "col":
                            self.Expect(TokenKind.Colon, ":")
                            langinfo = self.Expect(TokenKind.Number, "a number")
                            self.Expect(TokenKind.Comma, ",")
                            funcinfo["col"] = int(langinfo.Value)  
                        elif Item.Value == "external":
                            self.Expect(TokenKind.Colon, ":")
                            langinfo = self.Expect(TokenKind.Number, "a number")
                            self.Expect(TokenKind.Comma, ",")
                            funcinfo["external"] = int(langinfo.Value)
                        elif Item.Value == "type":
                            self.Expect(TokenKind.Colon, ":")
                            langinfo = self.Expect(TokenKind.Strings, "a string")
                            self.Expect(TokenKind.Comma, ",")
                            funcinfo["type"] = langinfo.Value
                        elif Item.Value == "void":
                            self.Expect(TokenKind.Colon, ":")
                            langinfo = self.Expect(TokenKind.Strings, "a string")
                            self.Expect(TokenKind.Comma, ",")
                            funcinfo["void"] = langinfo.Value
                        elif Item.Value == "params":
                            self.Expect(TokenKind.Colon, ":")
                            langinfo = self.Expect(TokenKind.Strings, "a string")
                            self.Expect(TokenKind.Comma, ",")
                            funcinfo["params"] = langinfo.Value
                        elif Item.Value == "ret":
                            self.Expect(TokenKind.Colon, ":")
                            langinfo = self.Expect(TokenKind.Strings, "a string")
                            self.Expect(TokenKind.Comma, ",")
                            funcinfo["ret"] = langinfo.Value
                        else:
                            print(f"[{Item.Line}:{Item.Start}:Error] '{Item.Value}' is not apart of the compuint metadata")
                            sys.exit(1)
                self.Expect(TokenKind.Cl_c_brack, "'}'")
                return {
                    "Kind" : "Function_debug",
                    "Size" : "?",
                    "Type" : ["?"],
                    "Info" : funcinfo,
                }
            
            elif debugging.Kind == TokenKind.File:
                fileinfo = {"name" : "", "val" : 2}
                
                self.Expect(TokenKind.Op_c_brack, "{")
                while self.CToken().Kind != TokenKind.EOF and self.CToken().Kind != TokenKind.Cl_c_brack:
                    if self.CToken().Kind == TokenKind.EOF:
                        print("Eof Error", sys.stderr)
                        sys.exit(1)
                    elif self.CToken().Kind == TokenKind.Cl_c_brack:
                        break
                    else:
                        Item = self.Expect(TokenKind.Strings, "a string")
                        
                        if Item.Value == "name":
                            self.Expect(TokenKind.Colon, ":")
                            prodinfo = self.Expect(TokenKind.Strings, " a string")
                            self.Expect(TokenKind.Comma, ",")
                            fileinfo["name"] = prodinfo.Value
                        elif Item.Value == "val":
                            self.Expect(TokenKind.Colon, ":")
                            langinfo = self.Expect(TokenKind.Number, "a number")
                            self.Expect(TokenKind.Comma, ",")
                            fileinfo["val"] = int(langinfo.Value)
                        else:
                            print(f"[{Item.Line}:{Item.Start}:Error] '{Item.Value}' is not apart of the compuint metadata")

                self.Expect(TokenKind.Cl_c_brack, "'}'")
                

                return {
                    "Kind" : "file_debug",
                    "Size" : "?",
                    "Type" : ["?"],
                    "Info" : fileinfo,
                }
            elif debugging.Kind == TokenKind.Mark:
                Name : str =  self.Expect(TokenKind.Strings, "a string").Value


                File = int(self.Expect(TokenKind.Number, "a number").Value)
                Line = int(self.Expect(TokenKind.Number, "a number").Value)
                Col = int(self.Expect(TokenKind.Number, "a number").Value)
                    
                self.marks.update({Name : f"{File} {Line} {Col}"})
                return {
                    "Kind" : "Marking",
                    "Size" : "?",
                    "Type" : ["?"],
                }

        elif met.Value == "?file":
            return {
                "Kind" : "Fileset",
                "Size" : "?",
                "Type" : ["?"],
                "Name" : self.Expect(TokenKind.Strings, "a string").Value
            }
               
        elif met.Value == "?.m":
            GetLoc = self.marks.get(self.Adv().Value)
            
            return {
                "Kind" : "LocMark",
                "Size" : "?",
                "Type" : ["?"],
                "Loc" : GetLoc
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
        else: 
            print(f"{self.Adv().Value} <- why is this here", file=sys.stderr)
            sys.exit(1)


