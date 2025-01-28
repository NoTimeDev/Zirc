section .data  
section .text
    global main 
    extern exit
    default rel

main:
	push rbp
	mov rbp, rsp
	sub rsp, 16

	mov rcx, 3
	mov rbx, 4
	add rcx, rbx
	
    mov rax, 4
	mov rbx, 5
	add rax, rbx
	
    mov rbx, 5
	mov [rbp-8], rcx
	mov rcx, 6
	add rbx, rcx
	
    mov rcx, [rbp-8]
	mov [rbp-16], rax
	mov rax, 5
	add rax, rcx
	
    mov rsp, rbp
	pop rbp

    mov rdi, 8 
    call exit wrt ..plt
    ret

