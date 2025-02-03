;Zirc on: Linux
;Zed Compiler Project
default rel
bits 64
section .rodata
	fl0 dd 4.5
	fl1 dd 5.5
section .data
;section .extern
extern _exit
section .text
	global main
main:
	push rbp
	mov rbp, rsp
	sub rsp, 16
	movss xmm0, [fl0]
	movss xmm1, [fl1]
	addss xmm0, xmm1
	cvttss2si rcx, xmm0
	xor rdi, rdi
	mov edi, ecx
	mov rsp, rbp
	pop rbp
	call _exit wrt ..plt