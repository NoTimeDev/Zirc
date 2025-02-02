import platform
Sys_Os = platform.system()

class CodeGen:
    def __init__(self, Ast: list[dict]):
        self.Ast: list[dict] = Ast
                
        self.Pos: int = 0
        
        self.ExternalFunc: list[str] = []
        
        if Sys_Os == "Linux":
            self.Headers: list[str] = [";Zirc on: Linux", ";Zed Compiler Project", "default rel", "bits 64"]
        elif Sys_Os == "Windows":
            self.Headers: list[str] = [";Zirc on: Windows", "\n;Zed Compiler Project", "default rel", "bits 64"]
            
        self.Data: list[str] = ["section .data"]
        self.Extern: list[str] = [";section .extern"]
        self.Text: list[str] = ["section .text"]
        
        self.Body: list[str] = []
            
        self.Comment: str = ""
        self.NumSize: str = "i64"

        self.Di: int = 0
        self.Hi: int = 0
        self.Ti: int = 0
        self.Bi: int = 0
        self.Ei: int = 0
            
        self.AllocSpace: int = 0
   
        self.Temporay_Vars: dict = {}
        
        self.Reg64: list[str] = ["rcx", "rbx", "rax", "rdi"]
        self.Reg32: list[str] = ["ecx", "ebx", "eax", "edi"]
        self.Reg16: list[str] = ["cx", "bx", "ax", "di"]
        self.Reg8: list[str] = ["cl", "bl", "al", "dil"]
        
        self.UReg64: list[str] = []
        self.UReg32: list[str] = []
        self.UReg16: list[str] = []
        self.UReg8: list[str] = []
        
        self.RegMap = {
            "1" : ['rcx','ecx', 'cx', "cl"],
            "2" : ['rbx', 'ebx', 'bx', "bl"],
            "3" : ['rax', 'eax', 'ax', "bl"],
            "4" : ["rdi", "edi", "di", "dil"]

        }
        
        self.MapTypeToSize = {
            "i64" : "qword",
            "i32" : "dword",
            "i16" : "word",
            "i8" : "byte"
        }
        self.InMain = False 
        self.InMainSize = ""
        self.Loc = 0
    def OutData(self, info: str):
        if self.Comment != "":
            self.Data.append("\t" * self.Di + self.Comment); self.Comment = ""
        self.Data.append("\t" * self.Di + info)

    def OutHead(self, info: str):
        if self.Comment != "":
            self.Headers.append("\t" * self.Hi + self.Comment); self.Comment = ""
        self.Headers.append("\t" * self.Hi + info)


    def OutText(self, info: str):
        if self.Comment != "":
            self.Text.append("\t" * self.Ti + self.Comment); self.Comment = ""
        self.Text.append("\t" * self.Ti + info)


    def OutExtern(self, info: str):
        if self.Comment != "":
            self.Extern.append("\t" * self.Ei + self.Comment); self.Comment = ""
        self.Extern.append("\t" * self.Ei + info)


    def OutBody(self, info: str):
        if self.Comment != "":
            self.Body.append("\t" * self.Bi + self.Comment); self.Comment = ""
        self.Body.append("\t" * self.Bi + info)

    
    def Gen(self, Node):
        match Node.get("Kind"):
            case "Temp_Var":
                return self.GenVar(Node)
            case "Add-Inst":
                return self.GenAdd(Node)
            case "func-def":
                return self.GenFunc(Node)
            case "Integer":
                return self.GenInt(Node)
            case "asmcom":
                self.Comment = f";{Node.get("Comment")}"
            case "Call_Var":
                return self.CallVar(Node)
            case "Load-inst":
                return self.GenLoad(Node)
            case "Ret-inst":
                return self.GenRet(Node)
            case "Sext-inst":
                return self.GenSext(Node)
            case "Zext-inst":
                return self.GenZext(Node)
            case _:
                print(f"I Dont Support {Node.get("Kind")}")
    
    def RetSizeForType(self, Type):
        if Type == "i8":
            return "1"
        elif Type == "i16":
            return "2"
        elif Type == "i32":
            return "4"
        elif Type == "i64":
            return "8"

    def GenSext(self, Node):
        TempVar = self.Temporay_Vars.get(Node.get("Extending"))
        
        if TempVar["Register"][0] != "[":
            RegInfo = self.GetPosMap(TempVar["Register"])
        
            poses = { "i64" : 0, "i32" : 1, "i16" : 2, "i8" : 3 }

            ExtendingReg = RegInfo[poses.get(Node.get("Type")[0])]
            if Node.get("Type")[0] == "i64" and Node.get("From")[0] == "i32" or Node.get("Type")[0] == "i32" and Node.get("From")[0] == "i64":
                self.OutBody(f"movsxd {ExtendingReg}, {self.MapTypeToSize[Node.get("From")[0]]} {TempVar["Register"]}")
            else:
                self.OutBody(f"movsx {ExtendingReg}, {self.MapTypeToSize[Node.get("From")[0]]} {TempVar["Register"]}")

            self.Temporay_Vars.update({Node.get("Extending"): {
                "Register" : ExtendingReg,
                "Type" : Node.get("Type"),
                "Size" : self.GetSizeForReg(ExtendingReg),
                "Should_Load" : TempVar.get("Should_Load")
            }})
            
        else:
            Reg = self.GetReg(self.RetSizeForType(Node.get("Type")[0]))
            RegInfo = self.GetPosMap(Reg)
        

            if Node.get("Type")[0] == "i64" and Node.get("From")[0] == "i32" or Node.get("Type")[0] == "i32" and Node.get("From")[0] == "i64":
                self.OutBody(f"movsxd {Reg}, {self.MapTypeToSize[Node.get("From")[0]]} {TempVar["Register"]}")
            else:
                self.OutBody(f"movsx {Reg}, {self.MapTypeToSize[Node.get("From")[0]]} {TempVar["Register"]}")

            self.Temporay_Vars.update({Node.get("Extending"): {
                "Register" : Reg,
                "Type" : Node.get("Type"),
                "Size" : self.GetSizeForReg(Reg),
                "Should_Load" : TempVar.get("Should_Load")
            }})
                
    def GenZext(self, Node):
        TempVar = self.Temporay_Vars.get(Node.get("Extending"))
        
        if TempVar["Register"][0] != "[":
            RegInfo = self.GetPosMap(TempVar["Register"])
        

            poses = { "i64" : 0, "i32" : 1, "i16" : 2, "i8" : 3 }
            
            ExtendingReg = RegInfo[poses.get(Node.get("Type")[0])]
            if Node.get("Type")[0] == "i64" and Node.get("From")[0] == "i32" or Node.get("Type")[0] == "i32" and Node.get("From")[0] == "i64":
                self.OutBody(f"xor {ExtendingReg}, {ExtendingReg}")
                self.OutBody(f"mov {RegInfo[poses.get(Node.get("From"))]}, {TempVar["Register"]}")
                self.OutBody(f"mov {ExtendingReg}, {ExtendingReg}")
            else:
                self.OutBody(f"movzx {ExtendingReg}, {self.MapTypeToSize[Node.get("From")[0]]} {TempVar["Register"]}")

            self.Temporay_Vars.update({Node.get("Extending"): {
                "Register" : ExtendingReg,
                "Type" : Node.get("Type"),
                "Size" : self.GetSizeForReg(ExtendingReg),
                "Should_Load" : TempVar.get("Should_Load")
            }})
            
        else:
            Reg = self.GetReg(self.RetSizeForType(Node.get("Type")[0]))
            RegInfo = self.GetPosMap(Reg)
        

            poses = { "i64" : 0, "i32" : 1, "i16" : 2, "i8" : 3 }
            print(RegInfo)

            if Node.get("Type")[0] == "i64" and Node.get("From")[0] == "i32" or Node.get("Type")[0] == "i32" and Node.get("From")[0] == "i64":
                self.OutBody(f"mov {Reg}, {TempVar["Register"]}")
            else:
                self.OutBody(f"movzx {Reg}, {self.MapTypeToSize[Node.get("From")[0]]} {TempVar["Register"]}")

            self.Temporay_Vars.update({Node.get("Extending"): {
                "Register" : Reg,
                "Type" : Node.get("Type"),
                "Size" : self.GetSizeForReg(Reg),
                "Should_Load" : TempVar.get("Should_Load")
            }})
    

    def GetPosMap(self, Reg):
        for i in list(self.RegMap.keys()):
            if Reg in self.RegMap.get(i):
                return self.RegMap.get(i)
           
        return [Reg]
    
    def GetSizeForReg(self, Reg):
        if Reg in self.Reg64 or Reg in self.UReg64:
            return "8"
        if Reg in self.Reg32 or Reg in self.UReg32:
            return "4"
        if Reg in self.Reg16 or Reg in self.UReg16:
            return "2"
        if Reg in self.Reg8 or Reg in self.UReg8:
            return "1"
        
        
    def IfOnein(self, List1, List2):
        for i in List1:
            for i1 in List2:
                if i == i1:
                    return True
        return False

    def EnsureFreeReg(self, RegName, Size): 
        URegList = getattr(self, f"UReg{str( Size * 8 )}")
        RegList64_8 = self.GetPosMap(RegName)
        if self.IfOnein(URegList, RegList64_8):
            TempVar = {}
            Name = ""
            for i in list(self.Temporay_Vars.keys()):
                if self.Temporay_Vars.get(i).get("Register") in RegList64_8:
                    TempVar = self.Temporay_Vars.get(i)
                    Name = i 
                    break
                if TempVar != {}:
                    break
            
            self.AllocSpace+=int(self.GetSizeForReg(RegName))
            self.OutBody(f"mov [rbp-{self.AllocSpace}], {RegName}")
            self.Temporay_Vars.update({Name: {
                "Register" : f'[rbp-{self.AllocSpace}]',
                "Type" : TempVar.get("Type"),
                "Size" : TempVar.get("Size"),
                "Should_Load" : TempVar.get("Should_Load")
            }})

           
            self.GiveReg(RegName)

    def GenRet(self, Node):
        if Sys_Os == "Linux":
            if self.InMain == True:
                if "_exit" not in self.ExternalFunc:
                    self.ExternalFunc.append("_exit")
                    Com = self.Comment 
                    self.OutExtern(f"extern _exit")
                    self.Comment = Com
            
                self.NumSize = self.RetSizeForType(self.InMainSize)
                Returning = self.Gen(Node.get("Return"))
                self.EnsureFreeReg("rdi", 8)
            
                self.OutBody("mov rsp, rbp")
                self.OutBody("pop rbp")
                self.Body[self.Loc] = self.Bi  * "\t" + f"sub rsp, {self.AllocSpace}"

  
            
                if self.InMainSize == "i64":
                    self.OutBody(f"mov rdi, {Returning}")
                elif self.InMainSize == "i32":
                    self.OutBody(f"mov edi, {Returning}")
                elif self.InMainSize == "i16":
                    self.OutBody(f"mov di, {Returning}")
                elif self.InMainSize == "i8":
                    self.OutBody(f"mov dil, {Returning}")
                self.OutBody("call _exit wrt ..plt")
            
            else:
                pass 
        if Sys_Os == "Windows":
            if self.InMain == True:
                if "ExitProcess" not in self.ExternalFunc:
                    self.ExternalFunc.append("ExitProcess")
                    Com = self.Comment 
                    self.OutExtern(f"extern ExitProcess")
                    self.Comment = Com
            
                self.NumSize = self.RetSizeForType(self.InMainSize)
                Returning = self.Gen(Node.get("Return"))
                self.EnsureFreeReg("rcx", 8)
            
                self.OutBody("mov rsp, rbp")
                self.OutBody("pop rbp")
                self.Body[self.Loc] = self.Bi  * "\t" + f"sub rsp, {self.AllocSpace}"

  
            
                if self.InMainSize == "i64":
                    self.OutBody(f"mov rcx, {Returning}")
                elif self.InMainSize == "i32":
                    self.OutBody(f"mov ecx, {Returning}")
                elif self.InMainSize == "i16":
                    self.OutBody(f"mov cx, {Returning}")
                elif self.InMainSize == "i8":
                    self.OutBody(f"mov cl, {Returning}")
                self.OutBody("call ExitProcess")
            
            else:
                pass 


    def GenLoad(self, Node):
        NewName = Node.get("NewName")
        Getting = self.Temporay_Vars.get(Node.get("Loading")) 
        if Getting.get("Register")[0] != "[":
            self.Temporay_Vars.update({NewName : {
                "Register" : Getting.get("Register"),
                "Type" : Node.get("Type"),
                "Size" : Node.get("Size"),
                "Should_Load" : True,
            }})
            #from json import dumps 
            #print(dumps(self.Temporay_Vars, indent=4))  
            return Getting.get("Register")
        else:
            reg = self.GetReg(Node.get("Size"))
            self.OutBody(f"mov {reg}, {Getting.get("Register")}")
            self.Temporay_Vars.update({NewName : {
                "Register" : reg,
                "Type" : Node.get("Size"),
                "Size" : Node.get("Size"),
                "Should_Load" : True
            }})           
            
            return reg 
        
    def CallVar(self, Node):
        Loaded_Var: dict = self.Temporay_Vars.get(Node.get("Name"))

        if Loaded_Var.get("Register", "")[0] != "[":
            #print(self.UReg64, Node.get("Name"), "l")
            return Loaded_Var.get("Register")

        elif Loaded_Var.get("Register", "")[0] == "[" and Loaded_Var.get("Should_Load") == True:
            reg = self.GetReg(Loaded_Var.get("Size", ""))
            self.OutBody(f"mov {reg}, {Loaded_Var.get("Register")}")
            self.Temporay_Vars.update({Node.get("Name") : {
                "Register" : reg,
                "Type" : Node.get("Type"),
                "Size" : Node.get("Size"),
                "Should_Load" : True
            }})
       
            return reg
        else:
            return Loaded_Var.get("Register")
    

    def GetReg(self, Size):
        RegisterList: list[str] = getattr(self, f"Reg{str( int(Size) * 8 )}")
        URegisterList: list[str] = getattr(self, f"UReg{str( int(Size) * 8 )}")
        
        def AddAll():
            self.UReg64.append(self.Reg64.pop(0))
            self.UReg32.append(self.Reg32.pop(0))
            self.UReg16.append(self.Reg16.pop(0))
            self.UReg8.append(self.Reg8.pop(0))
                
        if len(RegisterList) == 0:

            Register = ""
            TempVar = {}
            Name = ""
            
            for i in list(self.Temporay_Vars.keys()):
                if self.Temporay_Vars.get(i).get("Register")[0] != "[":
                    Name = i 
                    Register = self.Temporay_Vars.get(i).get("Register")
                    TempVar = self.Temporay_Vars.get(i)
                    break 
                
                if Register != "":
                    break
            
            
            RegInfo = self.GetPosMap(Register)

            self.AllocSpace+=int(self.GetSizeForReg(Register))

            self.OutBody(f"mov [rbp-{self.AllocSpace}], {Register}")
            #print(Name, f"[rbp-{self.AllocSpace}]")
            self.GiveReg(Register)
            self.Temporay_Vars.update({Name : {
                "Register" : f"[rbp-{self.AllocSpace}]",
                "Type" : TempVar.get("Type"),
                "Size" : TempVar.get("Size"),
                "Should_Load" : TempVar.get("Should_Load")
            }})
            
            return RegisterList[-1]
        else:
            AddAll()

            reg = URegisterList[-1]
            
            Moved = ""
            for i in list(self.Temporay_Vars.keys()):
                if self.Temporay_Vars.get(i).get("Register") == reg:
                    if Moved == "":
                        self.AllocSpace+=int(self.GetSizeForReg(reg))
                        self.OutBody(f"mov [rbp-{self.AllocSpace}], {reg}")
                        Moved = f"[rbp-{self.AllocSpace}]"
                    TempVar = self.Temporay_Vars.get(i)
                    self.Temporay_Vars.update({i : {
                        "Register" : Moved,
                        "Type" : TempVar.get("Type"),
                        "Size" : TempVar.get("Size"),
                        "Should_Load" : TempVar.get("Should_Load")
                    }})

            return reg
    

    def GenInt(self, Node):

        Reg = self.GetReg(self.NumSize)
        
        self.OutBody(f"mov {Reg}, {Node.get("Value")}")
        return Reg 

    def GenFunc(self, Node):
        self.OutBody(f"{Node.get("Name")[1:]}:")
        if Node.get("Name") == "@main":
            self.InMain = True
            self.InMainSize = Node.get("Type")[0]
        self.Ti+=1
        self.OutText(f"global {Node.get("Name")[1:]}")
        self.Ti-=1
        
        self.Bi+=1
       
        #Set UP Stack Frame
        self.OutBody(f"push rbp")
        self.OutBody(f"mov rbp, rsp")
        self.OutBody(f"---Space---")

        self.Loc = len(self.Body) - 1
            
        for i in Node.get("Params"):
            #Handle arguments later on ohh boy i cant wait
            pass

        for i in Node.get("Body"):
            self.Gen(i)

        
        #-----------------
        
        self.Bi-=1
    
    def GiveReg(self, Reg):
        if Reg in self.UReg64:
            Pos = self.UReg64.index(Reg)

            
            self.Reg64.append(self.UReg64.pop(Pos))
            self.Reg32.append(self.UReg32.pop(Pos))
            self.Reg16.append(self.UReg16.pop(Pos))
            self.Reg8.append(self.UReg8.pop(Pos))
        elif Reg in self.UReg32:
            Pos = self.UReg32.index(Reg)

            
            self.Reg64.append(self.UReg64.pop(Pos))
            self.Reg32.append(self.UReg32.pop(Pos))
            self.Reg16.append(self.UReg16.pop(Pos))
            self.Reg8.append(self.UReg8.pop(Pos))

        elif Reg in self.UReg16:
            Pos = self.UReg16.index(Reg)

            
            self.Reg64.append(self.UReg64.pop(Pos))
            self.Reg32.append(self.UReg32.pop(Pos))
            self.Reg16.append(self.UReg16.pop(Pos))
            self.Reg8.append(self.UReg8.pop(Pos))

        elif Reg in self.UReg8:
            Pos = self.UReg8.index(Reg)

            
            self.Reg64.append(self.UReg64.pop(Pos))
            self.Reg32.append(self.UReg32.pop(Pos))
            self.Reg16.append(self.UReg16.pop(Pos))
            self.Reg8.append(self.UReg8.pop(Pos))

   
    def GenVar(self, Node):
        Val = self.Gen(Node.get("Value"))
        self.Temporay_Vars.update({Node.get("Name") : {
            "Register" : Val,
            "Type" : Node.get("Type"),
            "Size" : Node.get("Size"),
            "Should_Load" : False
        }})
       #print(self.UReg64[-1], Val, Node.get('Name'))
    def GenAdd(self, Node): 
        self.NumSize = Node.get("Size")

        Op1 = self.Gen(Node.get("Op1"))
        Op2 = self.Gen(Node.get("Op2"))
        

        self.OutBody(f"add {Op1}, {Op2}")
        self.GiveReg(Op2)
        return Op1 

    def GenAsm(self) -> str:
        while self.Pos < len(self.Ast): 
            self.Gen(self.Ast[self.Pos])
            self.Pos+=1

        return '\n'.join(self.Headers) + "\n" + '\n'.join(self.Data) + "\n" +  '\n'.join(self.Extern) + "\n" +  '\n'.join(self.Text) + "\n" +  '\n'.join(self.Body)      

