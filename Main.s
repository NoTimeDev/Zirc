# ┌---------------------------------┐
# |   Zura Syntax by TheDevConnor   |
# |   assembly by Soviet Pancakes   |
# └---------------------------------┘
# 
# What's New: Memory allocated / freed

# Everything beyond this point was generated automatically by the Zura compiler.
.att_syntax
.file "Test.zu"
.text
.globl _start
.file 0 "/home/devvy/Projects/Zirc" "Test.zu"
.Ltext0:
.weak .Ltext0
_start:
  call main
  xorq %rdi, %rdi
  movq $60, %rax
  syscall
.loc 0 1 6
	
.Ldie1_debug_start:
	
.type main, @function
.globl main

main:
	.loc 0 1 17
	.cfi_startproc
	pushq %rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq %rsp, %rbp
	.cfi_def_cfa_register 6
	.loc 0 1 26
	.loc 0 2 11
	.loc 0 2 13
	movq $3, %rdi
	movq $60, %rax
	syscall # SYS_EXIT
	popq %rbp
	ret
	.Ldie1_debug_end:
.cfi_endproc
.size main, .-main
	.Ldebug_text0:
.section	.debug_info,"",@progbits
	
.long .Ldebug_end -  .Ldebug_info
.Ldebug_info:
.weak .Ldebug_info
.word 0x5
.byte 0x1
.byte 0x8
.long .Ldebug_abbrev

.uleb128 1
.long .Ldebug_producer_string - .Ldebug_str_start
.short 0x8042
.long .Ldebug_file_string - .Ldebug_line_str_start
.long .Ldebug_file_dir - .Ldebug_line_str_start
.quad .Ltext0
.quad .Ldebug_text0 - .Ltext0
.long .Ldebug_line0
.uleb128 2
.byte 1
.long .Lmain_string
.byte 0
.byte 1
.byte 17
.long .Lint_debug_type
.quad .Ldie1_debug_start
.quad .Ldie1_debug_end - .Ldie1_debug_start
.uleb128 0x01
.byte 0x9c
.byte 0


.Lint_debug_type:
.uleb128 13
.byte 8
.byte 5
.string "int"
.Llong_debug_type:
.uleb128 13
.byte 4
.byte 7
.string "long"
.Lbool_debug_type:
.uleb128 13
.byte 1
.byte 0x02
.string "bool"
.Lfloat_debug_type:
.uleb128 13
.byte 4
.byte 4
.string "float"
.Lstr_debug_type:
.uleb128 14
.byte 8
.long .Lchar_debug_type
.Lchar_debug_type:
.uleb128 13
.byte 1
.byte 6
.string "char"
.byte 0
.Ldebug_end:
.section .debug_abbrev,"",@progbits
.Ldebug_abbrev:

.uleb128 1
.uleb128 0x11 # TAG_compile_unit
.byte	0x1 # No children
.uleb128 0x25 # AT_producer
.uleb128 0xe # FORM_strp
.uleb128 0x13 # AT_language
.uleb128 0x05 # FORM_data2
.uleb128 0x3 # AT_name
.uleb128 0x1f # FORM_line_strp
.uleb128 0x1b # AT_comp_dir
.uleb128 0x1f # FORM_line_strp
.uleb128 0x11 # AT_low_pc
.uleb128 0x1 # FORM_addr
.uleb128 0x12 # AT_high_pc
.uleb128 0x7 # FORM_data8
.uleb128 0x10 # AT_stmt_list
.uleb128 0x17 # FORM_sec_offset
.byte 0
.byte 0

.uleb128 2
.uleb128 0x2e # TAG_subprogram - FunctionNoParams, non-void
.byte 0x1 # Has children
.uleb128 0x3f # AT_external
.uleb128 0xc # FORM_flag_present
.uleb128 0x3 # AT_name
.uleb128 0xe # FORM_strp
.uleb128 0x3a # AT_decl_file
.uleb128 0xb # FORM_data1
.uleb128 0x3b # AT_decl_line
.uleb128 0xb # FORM_data1
.uleb128 0x39 # AT_decl_column
.uleb128 0xb # FORM_data1
.uleb128 0x49 # AT_type
.uleb128 0x13 # FORM_ref4
.uleb128 0x11 # AT_low_pc
.uleb128 0x1 # FORM_addr
.uleb128 0x12 # AT_high_pc
.uleb128 0x7 # FORM_data8
.uleb128 0x40 # AT_frame_base
.uleb128 0x18 # FORM_exprloc
.uleb128 0x7a # AT_call_all_calls
.uleb128 0x19 # FORM_flag_present

.byte 0
.byte 0

.uleb128 13
.uleb128 0x24 # TAG_base_type
.byte	0 # no children
.uleb128 0xb # AT_byte_size
.uleb128 0xb # FORM_data1
.uleb128 0x3e # AT_encoding
.uleb128 0xb # FORM_data1
.uleb128 0x3 # AT_name
.uleb128 0x8 # FORM_string

.byte 0
.byte 0

.uleb128 14
.uleb128 0xF # TAG_pointer_type
.byte 0 # No children
.uleb128 0xB # AT_byte_size
.uleb128 0xb # FORM_data1
.uleb128 0x49 #  AT_type
.uleb128 0x13 #  FORM_ref4
.byte 0
.byte 0
.byte 0
.byte 0
.section .debug_line,"",@progbits
.Ldebug_line0:
.section .debug_str,"MS",@progbits,1
.Ldebug_str_start:
.Ldebug_producer_string: .string "Zura compiler "

.Lmain_string:
	.string "main"

.section .debug_line_str,"MS",@progbits,1
.Ldebug_line_str_start:
.Ldebug_file_string: .string "Test.zu"
.Ldebug_file_dir: .string "Test.zu"
