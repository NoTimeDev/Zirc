#THIS IS THE LINUX VERSION OF ZIRC KEEP THIS IN MIND

class CodeGen:
    def __init__(self, Ast: dict):
        self.Ast: dict = Ast
        self.Pos: int = 0
        
        self.DataI: int = 0
        self.ExternsI: int = 1
        self.MainI: int = 0
        self.TextI: int = 0

        self.Headers: list[str] = ["default rel", "bits 64"]
        
        self.AllocateSpace = 0

        self.Main: list[str] = [""]
        
        self.Externs: list[str] = ["    extern _exit"]
        
        self.Text: list[str] = ["section .text"]
        self.Data: list[str] = ["section .data"]
        
        self.InMain:bool = False 
            
        self.Reg_64: list[str] = ["rcx", "rbx", "rax"]
        self.Reg_32: list[str] = ["ecx", 'ebx', "eax"]
        self.Reg_16: list[str] = ["cx", "bx", "ax"]
        self.Reg_8: list[str] = ["cl", "bl", "al"]
        
        self.UReg_64: list[str] = []
        self.UReg_32: list[str] = []
        self.UReg_16: list[str] = []
        self.UReg_8: list[str] = []
        
        self.Stored_Vars: dict[str, str] = {}
        self.Loaded_Vars: dict[str,str] = {}

        self.NumSize: str = ""

    def OutText(self, info):
        self.Text.append("\t" * self.TextI + info)

    def OutData(self, info):
        self.Data.append("\t" * self.DataI + info)

    def OutExtern(self, info):
        self.Data.append("\t" * self.ExternsI + info)

    def OutMain(self, info):
        self.Main.append("\t" * self.MainI + info)

    def GetNode(self):
        n =  self.Ast['Body'][self.Pos]
        self.Pos+=1
        return n 

    def GetAsm(self) -> str:
        while self.Pos < len(self.Ast.get("Body")):
            self.Gen(self.GetNode())
    
        return '\n'.join(self.Headers) + '\n' + '\n'.join(self.Data) + '\n' + '\n'.join(self.Text) + '\n' +"\n".join(self.Externs) + '\n'  + "\n".join(self.Main)
    def Gen(self, Node) -> str:
        if Node.get("Kind") == "Function":
            return self.GenFuction(Node)
        elif Node.get("Kind") == "TempVariable":
            return self.HandleTempVar(Node)
        elif Node.get("Kind") == "Add inst":
            return self.Addinst(Node)
        elif Node.get("Kind") == "Integer":
            return self.Loadint(Node)
        elif Node.get("Kind") == "Load inst":
            return self.Loadinst(Node)
        elif Node.get("Kind") == "CallTempVar":
            return self.CallTempVar(Node)
    
    def CallTempVar(self, Node):
        return self.Loaded_Vars.get(Node.get("Name"))
    def Loadinst(self, Node):
        stored = self.Stored_Vars.get(Node.get("Loading"))

        if stored[0] == '[':
            size = stored[stored.index("-") + 1: -1]
            if int(size) % 8 == 0:
                Reg = self.GetReg("i64")
                self.OutMain(f"mov {Reg}, {stored}")
            elif int(size) % 4 == 0:
                Reg = self.GetReg("i32")
                self.OutMain(f"mov {Reg}, {stored}")
            elif int(size) % 2 == 0:
                Reg = self.GetReg("i16")
                self.OutMain(f"mov {Reg}, {stored}")
            elif int(size) % 1 == 0:
                Reg = self.GetReg("i8")
                self.OutMain(f"mov {Reg}, {stored}")
            self.Loaded_Vars.update({Node.get("NewName") : Reg})
            return Reg
        else:
            return stored


    def Loadint(self, Node):
        Reg = self.GetReg(self.NumSize)
        self.OutMain(f"mov {Reg}, {Node.get("Value")}")
        return Reg

    def GetReg(self, size):
        if len(self.Reg_64) == 0:
            self.AllocateSpace+=(int(size[1:]) // 8)
            Name = list(self.Stored_Vars.keys())[0]
            Tmp = self.Stored_Vars.pop(Name)
            
            self.OutMain(f"mov [rbp-{self.AllocateSpace}], {Tmp}")
            self.Stored_Vars.update({Name : f"[rbp-{self.AllocateSpace}]"})

            if Tmp in self.UReg_64:
                Pos = self.UReg_64.index(Tmp)
                self.Reg_64.append(self.UReg_64.pop(Pos))
                self.Reg_32.append(self.UReg_32.pop(Pos))
                self.Reg_16.append(self.UReg_16.pop(Pos))
                self.Reg_8.append(self.UReg_8.pop(Pos))
            elif Tmp in self.UReg_32:
                Pos = self.UReg_32.index(Tmp)
                self.Reg_64.append(self.UReg_64.pop(Pos))
                self.Reg_32.append(self.UReg_32.pop(Pos))
                self.Reg_16.append(self.UReg_16.pop(Pos))
                self.Reg_8.append(self.UReg_8.pop(Pos))

            elif Tmp in self.UReg_16:
                Pos = self.UReg_16.index(Tmp)
                self.Reg_64.append(self.UReg_64.pop(Pos))
                self.Reg_32.append(self.UReg_32.pop(Pos))
                self.Reg_16.append(self.UReg_16.pop(Pos))
                self.Reg_8.append(self.UReg_8.pop(Pos))

            elif Tmp in self.UReg_8:
                Pos = self.UReg_8.index(Tmp)
                self.Reg_64.append(self.UReg_64.pop(Pos))
                self.Reg_32.append(self.UReg_32.pop(Pos))
                self.Reg_16.append(self.UReg_16.pop(Pos))
                self.Reg_8.append(self.UReg_8.pop(Pos))



        def AddAll():
            self.UReg_64.append(self.Reg_64[0]) 
            self.UReg_32.append(self.Reg_32[0])
            self.UReg_16.append(self.Reg_16[0])
            self.UReg_8.append(self.Reg_8[0])

        if size == "i64":
            AddAll()
            return self.Reg_64.pop(0)
        elif size == "i32":
            AddAll()
            return self.Reg_32.pop(0) 
        elif size == "i16":
            AddAll()
            return self.Reg_16.pop(0) 
        elif size == "i8":
            AddAll()
            return self.Reg_8.pop(0)
                                                       
    def GiveReg(self, Pos):
        self.Reg_64.append(self.UReg_64.pop(Pos))
        self.Reg_32.append(self.UReg_32.pop(Pos))
        self.Reg_16.append(self.UReg_16.pop(Pos))
        self.Reg_8.append(self.UReg_8.pop(Pos))

    def Addinst(self, Node):
        self.NumSize = Node.get("Type").get("Type")

        Op1 = self.Gen(Node.get("Op1"))
        Op2 = self.Gen(Node.get("Op2"))
        
        Pos = len(self.UReg_32) - 1 
        
        self.OutMain(f"add {Op1}, {Op2}")
        
        self.GiveReg(Pos)
        return Op1 
    
    def HandleTempVar(self, Node):
        INode = Node.get("Value")
        Name = self.Gen(INode)
            
        self.Stored_Vars.update({Node.get("Name") : Name})
        
        return Name

    def GenFuction(self, Node):
        if Node.get("Name") == "@main":
            self.InMain == True 
        
        self.MainI+=1

        self.OutMain(f"{Node.get("Name")[1:]}:")
        #Later On Handle stuff likle agruments
 
        #Stack Frame 
        self.OutMain("push rbp")
        self.OutMain("mov rbp, rsp")
        self.OutMain("---Save---")
        
        AllocLoc = len(self.Main) - 1
        for i in Node.get("Body"):
            self.Gen(i)
        
        
        self.Main[AllocLoc] = f"\tsub rsp, {self.AllocateSpace}\n"
        self.OutMain("\nmov rsp, rbp")
        self.OutMain("pop ebp")

        return ""
