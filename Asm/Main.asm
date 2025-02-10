    .file "~/Projects/Zirc/Test/Main.zr"
    .text 
.Ltext0:
	.file 0 "/home/devvy/Projects/Zirc" "Asm/Test.c"
	.globl	main
	.type	main, @function
main:
.LFB0:
	.file 1 "Asm/Test.c"
	.loc 1 1 11
	.cfi_startproc
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	.loc 1 2 18
	mov	DWORD PTR -4[rbp], 90
	.loc 1 3 12
	mov	eax, 1
	.loc 1 4 1
	pop	rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc

.section .debug_info
    .byte 0x01 
    .byte 0x10
    .string "main"
    .byte 0x03
    .byte 0x0F

    .byte 0x52
    .byte "x"
    .byte 0x03
    .byte 

