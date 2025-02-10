import sys 
import platform

class CodeGen:
    def __init__(self, Ast: list[dict], Flags: list[str] = [], Info: dict = {}):
        self.Ast: list[dict] = Ast
        self.Flags: list[str] = Flags
        self.Pos: int = 0
        self.Info: dict = Info
        
        self.Funcsbgd = {}
    
        self.FGL: int = 0 
        
        self.DbgStrc: int  = 0 
        self.Debug: bool = "debug" in self.Flags
        
        self.Regs = ["rax", "rcx", "rdi", "rsi", "r8", "r10"]

        self.Dwc: int = 1

        self.Opsys: str = platform.system() 
            
        if self.Opsys == "Windows":
            self.Text: list[str] = ["#Zirc on Windows"]
        elif self.Opsys == "Linux":
            self.Text: list[str] = ["#Zirc on Linux"]
        else:
            self.Text: list[str] = ["#poh"]
            
        if self.Debug == True:
            self.DebugInfo: list[str] = [".Letext0:", "\t.section    .debug_info,\"\",@progbits"]
            self.DebugAbbr: list[str] = [".Ldebug_end:", "\t.section .debug_abbrev,\"\",@progbits", ".Ldebug_abbrev0:"]
            self.DebugLine: list[str] = ["\t.section .debug_line,\"\",@progbits", ".Ldebug_line0:"]
            self.DebugStr: list[str] = ["\t.section .debug_str,\"MS\",@progbits,1"]
            self.DebugLineStr: list[str] = ["\t.section .debug_line_str,\"MS\",@progbits,1"]
        else:
            self.DebugInfo: list[str] = []
            self.DebugAbbr: list[str] = []
            self.DebugLine: list[str] = []
            self.DebugStr: list[str] = []
            self.DebugLineStr: list[str] = []
        
    def init_secs(self):
        self.Text.append(f'.file "{self.Info.get("File")}"')
        self.Text.append(f".text")
        if self.Debug == True:
            self.Text.append(".Ltext0:")
            self.Text.append(f'\t.file 0 "{self.Info.get("Dir")}" "{self.Info.get("ProvFile")}"')
        
    def Gen(self) -> str:
        self.init_secs()
        while self.Pos < len(self.Ast):
            self.GenNode(self.Ast[self.Pos])
            self.Pos+=1
        
        String : str = '\n'.join(self.Text)

                
        String+="\n" + '\n'.join(self.DebugInfo)
        String+="\n" + '\n'.join(self.DebugAbbr)
        String+="\n" + '\n'.join(self.DebugLine)
        String+="\n" + '\n'.join(self.DebugStr)
        String+="\n" + '\n'.join(self.DebugLineStr)
        
        return String
    def GenNode(self, Node):
        CKind = Node.get("Kind")

        if CKind == "CompilationUnit_debug":
            return self.CompUint(Node)
        elif CKind == "file_debug":
            return self.Filedbg(Node)
        elif CKind == "Fileset":
            self.Text[1] = f".file \"{Node.get('Name')}\""
        elif CKind == "Marking":
            return 0 
        elif CKind == "LocMark":
            self.Text.append(f"\t.loc {Node.get('Loc')}")
        elif CKind == "func-def":
            return self.FuncDef(Node)
        else:
            print("What Is This -> " + CKind, file=sys.stderr)
    
    def FuncDef(self, Node):
        self.Text.append("\t.globl " + Node.get('Name')[1:])
        self.Text.append("\t.type " + Node.get('Name')[1:] + ", " + "@function")
        self.Text.append(Node.get('Name')[1:] + ":")
        self.Text.append(f".LFGS{self.FGL}:") #function genral label
        self.Funcsbgd.update({Node.get('Name') : {"Start" : f".LFGS{self.FGL}"}})
        self.FGL+=1 
        
        Pos: int = 0 
        if Node.get("Body")[0].get('Kind') == "LocMark":
            self.GenNode(Node.get("Body")[0])
            Pos+=1 

        self.Text.append("\t.cfi_startproc")
        self.Text.append("\tpushq %rbp")
        self.Text.append("\t.cfi_def_cfa_offset 16")
        self.Text.append("\t.cfi_offset 6, -16")
        self.Text.append("\t%rsp, %rbp")
        self.Text.append("\t.cfi_def_cfa_register 6")

        self.Text.append(f".LFGE{self.FGL}:")
        self.Text.append(f"\t.size {Node.get('Name')[1:]}, .-{Node.get('Name')[1:]}")
        self.Funcsbgd.update({Node.get('Name') : {"Start" : self.Funcsbgd.get(Node.get('Name')).get("Start"), "End" : f"LFGE{}"})
        
    def Filedbg(self, Node):
        self.Text.append(f"\t.file {Node['Info']['val']} \"{Node['Info']['name']}\"")
 
    def MakeDStr(self, Info):
        self.DebugStr.append(f".LDBGSTR{self.DbgStrc}:")
        self.DebugStr.append(f"\t.string \"{Info}\"\n")
        self.DbgStrc+=1 
        
    def CompUint(self, Node): 
        self.DebugInfo.append("#Compilation Unit")
        self.DebugInfo.append("\t.long .Ldebug_end - .Ldebug_info0")
        self.DebugInfo.append("\t.Ldebug_info0: ") 
        self.DebugInfo.append("\t.value 0x5")
        self.DebugInfo.append("\t.byte 0x1")
        self.DebugInfo.append("\t.byte 0x8")
        self.DebugInfo.append("\t.long .Ldebug_abbrev0\n")

            
        self.DebugAbbr.append(f"\t.uleb128 {hex(self.Dwc)}") 
        self.DebugAbbr.append('\t.uleb128 0x11')
        self.DebugAbbr.append('\t.byte 0x1')
        self.DebugAbbr.append('\t.uleb128 0x25')
        self.DebugAbbr.append('\t.uleb128 0xe')
        self.DebugAbbr.append('\t.uleb128 0x13')
        self.DebugAbbr.append('\t.uleb128 0xb')
        self.DebugAbbr.append('\t.uleb128 0x3')
        self.DebugAbbr.append('\t.uleb128 0x1f')
        self.DebugAbbr.append('\t.uleb128 0x1b')
        self.DebugAbbr.append('\t.uleb128 0x1f')
        self.DebugAbbr.append('\t.uleb128 0x11')
        self.DebugAbbr.append('\t.uleb128 0x1')
        self.DebugAbbr.append('\t.uleb128 0x12')
        self.DebugAbbr.append('\t.uleb128 0x7')
        self.DebugAbbr.append('\t.uleb128 0x10')
        self.DebugAbbr.append('\t.uleb128 0x17')
        self.DebugAbbr.append('\t.byte 0')
        self.DebugAbbr.append('\t.byte 0\n')       

        self.DebugInfo.append("#Dw_TAG_compile_unit")
        self.DebugInfo.append(f"\t.uleb128 {hex(self.Dwc)}") 
        self.DebugInfo.append(f"\t.long .LDBGSTR{self.DbgStrc}")
        self.MakeDStr(Node['Info']['Producer'])
        self.DebugInfo.append(f"\t.short 0x1b39")
        
        self.DebugInfo.append(f"\t.long .LDBGSTR{self.DbgStrc}")
        self.MakeDStr(self.Info['ProvFile'])
        
        self.DebugInfo.append(f"\t.long .LDBGSTR{self.DbgStrc}")
        self.MakeDStr(self.Info['Dir'])
        self.DebugInfo.append(f"\t.quad .Ltext0")
        self.DebugInfo.append(f"\t.quad .Letext0-.Ltext0")
        self.DebugInfo.append(f"\t.long .Ldebug_line0")
        
        
