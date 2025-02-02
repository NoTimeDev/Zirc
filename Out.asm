;Zirc on: Windows

;Zed Compiler Project
default rel
bits 64
section .data
;section .extern
extern ExitProcess
section .text
	global main
main:
	push rbp
	mov rbp, rsp
	sub rsp, 16
	mov ecx, 5
	mov ebx, 5
	add ecx, ebx
	mov eax, 5
	mov edi, 5
	add eax, edi
	mov ebx, 5
	mov edi, 5
	add ebx, edi
	mov edi, 5
	mov [rbp-4], ecx
	mov ecx, 5
	add edi, ecx
	mov ecx, 5
	mov [rbp-8], eax
	mov eax, 5
	add ecx, eax
	mov rax, [rbp-4]
	mov [rbp-16], rcx
	mov rsp, rbp
	pop rbp
	mov rcx, rax
	call ExitProcess