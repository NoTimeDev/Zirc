;Zirc on: Linux
;Zed Compiler Project
default rel
bits 64
section .data
;section .extern
;ret 0
extern _exit
section .text
	global main
main:
	push rbp
	mov rbp, rsp
	sub rsp, 0
	;$1 = add i64 3, 4
	mov rcx, 3
	mov rbx, 4
	add rcx, rbx
	;$2 = add i32 6, 7
	mov ecx, 6
	mov ebx, 7
	add ecx, ebx
	;$3 = add i16 3, 4
	mov cx, 3
	mov bx, 4
	add cx, bx
	;$4 = add i8 4, 5
	mov cl, 4
	mov bl, 5
	add cl, bl
	;ret 0
	mov al, 0
	mov rdi, al
	call _exit wrt ..plt
	mov rsp, rbp
	pop rbp
