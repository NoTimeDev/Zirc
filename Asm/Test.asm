	.file	"Test.c"
	.intel_syntax noprefix
# GNU C17 (GCC) version 14.2.1 20240910 (x86_64-pc-linux-gnu)
#	compiled by GNU C version 14.2.1 20240910, GMP version 6.3.0, MPFR version 4.2.1, MPC version 1.3.1, isl version isl-0.27-GMP

# GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
# options passed: -masm=intel -mtune=generic -march=x86-64 -O0 -fno-asynchronous-unwind-tables -fno-dwarf2-cfi-asm
	.text
	.globl	main
	.type	main, @function
main:
	push	rbp	#
	mov	rbp, rsp	#,
# Test.c:2:     int x  =9;
	mov	DWORD PTR -12[rbp], 9	# x,
# Test.c:3:     int y = 5 + x;
	mov	eax, DWORD PTR -12[rbp]	# tmp103, x
	add	eax, 5	# y_2,
	mov	DWORD PTR -8[rbp], eax	# y, y_2
# Test.c:4:     int p = 6 + 4;
	mov	DWORD PTR -4[rbp], 10	# p,
# Test.c:6:     return p;
	mov	eax, DWORD PTR -4[rbp]	# _4, p
# Test.c:7: }
	pop	rbp	#
	ret	
	.size	main, .-main
	.ident	"GCC: (GNU) 14.2.1 20240910"
	.section	.note.GNU-stack,"",@progbits
