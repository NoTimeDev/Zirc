#Zirc on Linux
.file "Main.zr"
.text
.Ltext0:
	.file 0 "/home/devvy/Projects/Zirc" "Test/Main.zr"
	.file 1 "Test/Main.zr"
	.loc 1 8 0
.Letext0:
	.section    .debug_info,"",@progbits
#Compilation Unit
	.long .Ldebug_end - .Ldebug_info0
	.Ldebug_info0: 
	.value 0x5
	.byte 0x1
	.byte 0x8
	.long .Ldebug_abbrev0

#Dw_TAG_compile_unit
	.uleb128 0x1
	.long .LDBGSTR0
	.short 0x1b39
	.long .LDBGSTR1
	.long .LDBGSTR2
	.quad .Ltext0
	.quad .Letext0-.Ltext0
	.long .Ldebug_line0
.Ldebug_end:
	.section .debug_abbrev,"",@progbits
.Ldebug_abbrev0:
	.uleb128 0x1
	.uleb128 0x11
	.byte 0x1
	.uleb128 0x25
	.uleb128 0xe
	.uleb128 0x13
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0x1f
	.uleb128 0x1b
	.uleb128 0x1f
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x10
	.uleb128 0x17
	.byte 0
	.byte 0

	.section .debug_line,"",@progbits
.Ldebug_line0:
	.section .debug_str,"MS",@progbits,1
.LDBGSTR0:
	.string "Zirc V1-0, Zed V1-0"

.LDBGSTR1:
	.string "Test/Main.zr"

.LDBGSTR2:
	.string "/home/devvy/Projects/Zirc"

	.section .debug_line_str,"MS",@progbits,1
