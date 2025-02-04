import platform
Sys_Os = platform.system()

def advanceto16(num):
    if num == 0:
        return 16
    while num % 16 != 0:
        num+=1 
    return num

class CodeGen:
    def __init__(self, Ast: list[dict]):
        self.Ast: list[dict] = Ast
                
        self.Pos: int = 0
        
        self.floatcount: int = 0 

        self.ExternalFunc: list[str] = []
        
        if Sys_Os == "Linux":
            self.Headers: list[str] = [";Zirc on: Linux", ";Zed Compiler Project", "default rel", "bits 64"]
        elif Sys_Os == "Windows":
            self.Headers: list[str] = [";Zirc on: Windows", "\n;Zed Compiler Project", "default rel", "bits 64"]
       
        self.RoData: list[str] = ["section .rodata"]
        self.Data: list[str] = ["section .data"]
        self.Extern: list[str] = [";section .extern"]
        self.Text: list[str] = ["section .text"]
        
        self.Body: list[str] = []
            
        self.Comment: str = ""
        self.NumSize: str = "i32"
        self.FloatSize: str = "f32"

        self.Di: int = 0
        self.Hi: int = 0
        self.Ti: int = 0
        self.Bi: int = 0
        self.Ei: int = 0
        self.Rdi: int = 0
            
        self.AllocSpace: int = 0
   
        self.Temporay_Vars: dict = {}
            
        self.FReg: list[str] = ["xmm0", "xmm1", "xmm2"] 
        self.UFReg: list[str] = []

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
            "3" : ['rax', 'eax', 'ax', "al"],
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

        self.IsInt = False
        self.IsFloat = False

    def OutRData(self, info: str):
        if self.Comment != "":
            self.RoData.append("\t" * self.Di + self.Comment); self.Comment = ""
        self.RoData.append("\t" * self.Rdi + info)

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
                self.Comment = f";{Node.get('Comment')}"
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
            case "Trunc-inst":
                return self.GenTrunc(Node)
            case "Fadd-Inst":
                return self.GenFadd(Node)
            case "Float":
                return self.GenFloat(Node)
            case "Fl-to-uint":
                return self.GenFlToUint(Node) 
            case _:
                print(f"I Dont Support {Node.get('Kind')}")

    def GenFlToUint(self, Node):
        TempVar = self.Temporay_Vars.get(Node.get("OgName"))
        
        if TempVar["Register"][0] != "[":
            poses = { "i64" : 0, "i32" : 1, "i16" : 2, "i8" : 3 }

            Reg = self.GetReg("8")

            self.OutBody(f'cvttss2si {Reg}, {TempVar["Register"]}')
            
            self.GiveFlReg(TempVar["Register"])
            RegInfo = self.GetPosMap(Reg)
            RReg = RegInfo[poses[Node.get("Type")[0]]]

            self.Temporay_Vars.update({Node.get("NewName"): {
                "Register" : RReg,
                "Type" : Node.get("Type"),
                "Size" : self.GetSizeForReg(RReg),
                "Should_Load" : TempVar.get("Should_Load"),
                "IsFloat" : True,
                "IsInt" : False
            }})
            
        else:
            fReg = self.GetFlReg()

            if Node.get("Size") == "4":
                self.OutBody(f'movss {fReg}, {TempVar.get("Register")}')
            elif Node.get("Size") == "8":
                self.OutBody(f'movsd {fReg}, {TempVar.get("Register")}')

            Reg = self.GetReg("8")

            
            poses = { "i64" : 0, "i32" : 1, "i16" : 2, "i8" : 3 }
            self.OutBody(f"cvttss2si {Reg}, {fReg}")
            
            self.GiveFlReg(fReg)
            RegInfo = self.GetPosMap(Reg)
        
            RReg = RegInfo[poses[Node.get("Type")[0]]]

            self.Temporay_Vars.update({Node.get("NewName"): {
                "Register" : RReg,
                "Type" : Node.get("Type"),
                "Size" : self.GetSizeForReg(RReg),
                "Should_Load" : TempVar.get("Should_Load"),
                "IsFloat" : True,
                "IsInt" : False
            }})
            

    def GiveFlReg(self, Reg):
        self.FReg.append(self.UFReg.pop(self.UFReg.index(Reg)))

    def GetFlReg(self):
        Name: str = ""
        Register: str = ""
        TempVar: str = ""

        if len(self.FReg) == 0:
            for i in list(self.Temporay_Vars.keys()):
                if self.Temporay_Vars.get(i).get("Register")[0] != "[":
                    Name = i 
                    Register = self.Temporay_Vars.get(i).get("Register")
                    TempVar = self.Temporay_Vars.get(i)
                    break 
                
                if Register != "":
                    break
            
            

            self.AllocSpace+=int(TempVar.get('Size'))
            
            if TempVar.get("Size") == "8":
                self.OutBody(f"movsd [rbp-{self.AllocSpace}], {Register}")
            elif TempVar.get("Size") == "4":
                self.OutBody(f"movss [rbp-{self.AllocSpace}], {Register}")
            #print(Name, f"[rbp-{self.AllocSpace}]")
            self.GiveFlReg(Register)
            self.Temporay_Vars.update({Name : {
                "Register" : f"[rbp-{self.AllocSpace}]",
                "Type" : TempVar.get("Type"),
                "Size" : TempVar.get("Size"),
                "Should_Load" : TempVar.get("Should_Load"),
                "IsInt" : False,
                "IsFloat" : True
            }})
            
            return Register

        else:
            reg = self.FReg.pop(0)
            self.UFReg.append(reg) 
            
            Moved = ""
            for i in list(self.Temporay_Vars.keys()):
                if self.Temporay_Vars.get(i).get("Register") == reg:
                    if Moved == "":
                        self.AllocSpace+=int(self.Temporay_Vars.get("Size"))
                        if self.Temporay_Vars.get("Size") == "4":
                            self.OutBody(f"movss [rbp-{self.AllocSpace}], {reg}")
                        else:
                            self.OutBody(f"movsd [rbp-{self.AllocSpace}], {reg}") 
                        Moved = f"[rbp-{self.AllocSpace}]"
                    TempVar = self.Temporay_Vars.get(i)
                    self.Temporay_Vars.update({i : {
                        "Register" : Moved,
                        "Type" : TempVar.get("Type"),
                        "Size" : TempVar.get("Size"),
                        "Should_Load" : TempVar.get("Should_Load"),
                        "IsInt" : False,
                        "IsFloat" : True 
                    }})

            
            return reg 

    def GenFloat(self, Node):
        self.IsFloat = True
        self.IsInt = False

        self.Rdi+=1 
        reg = self.GetFlReg()

        if self.FloatSize == "f64":
            self.OutRData(f'fl{self.floatcount} dq {Node.get("Value")}')
            self.OutBody(f"movsd {reg}, [fl{self.floatcount}]")
            self.floatcount+=1 
        elif self.FloatSize == "f32":
            self.OutRData(f'fl{self.floatcount} dd {Node.get("Value")}')
            self.OutBody(f"movss {reg}, [fl{self.floatcount}]")
            self.floatcount+=1

        self.Rdi-=1 
        return reg

    def GenFadd(self, Node):
        self.IsInt = False
        self.IsFloat = True

        self.FloatSize = Node.get("Type")[0]
        Op1 = self.Gen(Node.get("Op1"))
        Op2 = self.Gen(Node.get("Op2"))
        
        if Node.get("Type")[0] == "f32":
            self.OutBody(f"addss {Op1}, {Op2}")
        elif Node.get("Type")[0] == "f64":
            self.OutBody(f"addsd {Op1}, {Op2}")

        return Op1 
    def GenTrunc(self, Node):
        TempVar = self.Temporay_Vars.get(Node.get("Extending"))

        poses = { "i64" : 0, "i32" : 1, "i16" : 2, "i8" : 3 }
        if TempVar.get("Register")[0] != "[":    
            RegInfo = self.GetPosMap(TempVar["Register"])
            
            Reg = RegInfo[poses[Node.get("Type")[0]]]
            
            self.Temporay_Vars.update({Node.get("Extending"): {
                "Register" : Reg,
                "Type" : Node.get("Type"),
                "Size" : self.GetSizeForReg(Reg),
                "Should_Load" : TempVar.get("Should_Load")
            }})
        elif TempVar.get("Register")[0] == "[":
            Reg = self.GetReg(self.RetSizeForType(Node.get("From")[0]))
            RegInfo = self.GetPosMap(Reg)
            

            self.OutBody(f'mov {Reg}, {TempVar.get("Register")}')
            self.Temporay_Vars.update({Node.get("Extending"): {
                "Register" :  RegInfo[poses[Node.get("Type")[0]]],
                "Type" : Node.get("Type"),
                "Size" : self.GetSizeForReg(Reg),
                "Should_Load" : TempVar.get("Should_Load")
            }})

    def RetTypeForSize(self, Size):
        if Size == "1":
            return "i8"
        elif Size == "2":
            return "i16"
        elif Size == "4":
            return "i32"
        elif Size == "8":
            return "i64"

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
                self.OutBody(f'movsxd {ExtendingReg}, {self.MapTypeToSize[Node.get("From")[0]]} {TempVar["Register"]}')
            else:
                self.OutBody(f'movsx {ExtendingReg}, {self.MapTypeToSize[Node.get("From")[0]]} {TempVar["Register"]}')

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
                self.OutBody(f'movsxd {Reg}, {self.MapTypeToSize[Node.get("From")[0]]} {TempVar["Register"]}')
            else:
                self.OutBody(f'movsx {Reg}, {self.MapTypeToSize[Node.get("From")[0]]} {TempVar["Register"]}')

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
                self.OutBody(f'mov {RegInfo[poses.get(Node.get("From"))]}, {TempVar["Register"]}')
                self.OutBody(f"mov {ExtendingReg}, {ExtendingReg}")
            else:
                self.OutBody(f'movzx {ExtendingReg}, {self.MapTypeToSize[Node.get("From")[0]]} {TempVar["Register"]}')

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
                self.OutBody(f'mov {Reg}, {TempVar["Register"]}')
            else:
                self.OutBody(f'movzx {Reg}, {self.MapTypeToSize[Node.get("From")[0]]} {TempVar["Register"]}')

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
                self.NumSize = self.RetSizeForType(self.InMainSize)
                Returning = self.Gen(Node.get("Return"))
                self.EnsureFreeReg("rdi", 8)
            
        
                self.OutBody("xor rdi, rdi")
                if self.InMainSize == "i64":
                    self.OutBody(f"mov rdi, {Returning}")
                elif self.InMainSize == "i32":
                    self.OutBody(f"mov edi, {Returning}")
                elif self.InMainSize == "i16":
                    self.OutBody(f"mov di, {Returning}")
                elif self.InMainSize == "i8":
                    self.OutBody(f"mov dil, {Returning}")
                 
                self.OutBody("mov rsp, rbp")
                self.OutBody("pop rbp")
                self.Body[self.Loc] = self.Bi  * "\t" + f"sub rsp, {advanceto16(self.AllocSpace)}"
                self.OutBody("mov rax, 60")
                self.OutBody("syscall")
      
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
            
 
                self.OutBody(f"xor rcx, rcx") 
                if self.InMainSize == "i64":
                    self.OutBody(f"mov rcx, {Returning}")
                elif self.InMainSize == "i32":
                    self.OutBody(f"mov ecx, {Returning}")
                elif self.InMainSize == "i16":
                    self.OutBody(f"mov cx, {Returning}")
                elif self.InMainSize == "i8":
                    self.OutBody(f"mov cl, {Returning}")
                
                self.OutBody("mov rsp, rbp")
                self.OutBody("pop rbp")
                self.Body[self.Loc] = self.Bi  * "\t" + f"sub rsp, {advanceto16(self.AllocSpace)}"
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
                "IsInt" : Getting.get("IsInt"),
                "IsFloat" : Getting.get("IsFloat")
            }})
            #from json import dumps 
            #print(dumps(self.Temporay_Vars, indent=4))  
            return Getting.get("Register")
        else:
            if Getting.get("IsFloat") == True:
                reg = self.GetFlReg()
                if Getting.get("Size") == "4":
                    self.OutBody(f'movss {reg}, {Getting.get("Register")}')
                elif Getting.get("Size") == "8":
                    self.OutBody(f'movsd {reg}, {Getting.get("Register")}')
                self.Temporay_Vars.update({NewName : {
                    "Register" : reg,
                    "Type" : Node.get("Type"),
                    "Size" : Node.get("Size"),
                    "Should_Load" : True,
                    "IsInt" : True,
                    "IsFloat" : False
                
                }})           
            
                return reg 
            
            elif Getting.get("IsInt") == True:
                reg = self.GetReg(Node.get("Size"))
                self.OutBody(f'mov {reg}, {Getting.get("Register")}')
                self.Temporay_Vars.update({NewName : {
                    "Register" : reg,
                    "Type" : Node.get("Type"),
                    "Size" : Node.get("Size"),
                    "Should_Load" : True,
                    "IsInt" : True,
                    "IsFloat" : False
                
                }})           
            
                return reg 
        
    def CallVar(self, Node):
        Loaded_Var: dict = self.Temporay_Vars.get(Node.get("Name"))

        if Loaded_Var.get("Register", "")[0] != "[":
            #print(self.UReg64, Node.get("Name"), "l")
            return Loaded_Var.get("Register")

        elif Loaded_Var.get("Register", "")[0] == "[" and Loaded_Var.get("Should_Load") == True and Loaded_Var.get("IsInt") == True:
            reg = self.GetReg(Loaded_Var.get("Size", ""))
            self.OutBody(f'mov {reg}, {Loaded_Var.get("Register")}')
            self.Temporay_Vars.update({Node.get("Name") : {
                "Register" : reg,
                "Type" : Node.get("Type"),
                "Size" : Node.get("Size"),
                "Should_Load" : True,
                "IsInt" : True,
                "IsFloat" : False
            }})
       
            return reg 
        elif Loaded_Var.get("Register", "")[0] == "[" and Loaded_Var.get("Should_Load") == True and Loaded_Var.get("IsFloat") == True:
            reg = self.GetFlReg()
            
            if Loaded_Var.get("Size") == "4":
                self.OutBody(f'movss {reg}, {Loaded_Var.get("Register")}')
            elif Loaded_Var.get("Size") == 8:
                self.OutBody(f'movsd {reg}, {Loaded_Var.get("Register")}')

            self.Temporay_Vars.update({Node.get("Name") : {
                "Register" : reg,
                "Type" : Node.get("Type"),
                "Size" : Node.get("Size"),
                "Should_Load" : True,
                "IsInt" : False,
                "IsFloat" : True
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
                "Should_Load" : TempVar.get("Should_Load"),
                "IsInt" : True,
                "IsFloat" : False
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
                        "Should_Load" : TempVar.get("Should_Load"),
                        "IsInt" : True,
                        "IsFloat" : False 
                    }})

            return reg
    

    def GenInt(self, Node):
        self.IsInt = True
        self.IsFloat = False 

        Reg = self.GetReg(self.NumSize)
        
        if int(Node.get("Value")) <= -2147483649 or int(Node.get("Value")) >= 4294967296:
            self.OutBody(f'movabs {Reg}, {Node.get("Value")}')
        else:
            self.OutBody(f'mov {Reg}, {Node.get("Value")}')
        return Reg 

    def GenFunc(self, Node):
        self.OutBody(f'{Node.get("Name")[1:]}:')
        if Node.get("Name") == "@main":
            self.InMain = True
            self.InMainSize = Node.get("Type")[0]
        self.Ti+=1
        self.OutText(f'global {Node.get("Name")[1:]}')
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
            "Should_Load" : False,
            "IsInt" : self.IsInt,
            "IsFloat" : self.IsFloat,
        }})
       #print(self.UReg64[-1], Val, Node.get('Name'))
    def GenAdd(self, Node): 
        self.IsInt = True
        self.IsFloat = False

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

        return '\n'.join(self.Headers) + "\n" + '\n'.join(self.RoData) + '\n' + '\n'.join(self.Data) + "\n" +  '\n'.join(self.Extern) + "\n" +  '\n'.join(self.Text) + "\n" +  '\n'.join(self.Body)      

