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
# Test.c:4:     float x1 = 9.4;
	movss	xmm0, DWORD PTR .LC0[rip]	# tmp101,
	movss	DWORD PTR -16[rbp], xmm0	# x1, tmp101
# Test.c:5:     float x2 = 4.8;
	movss	xmm0, DWORD PTR .LC1[rip]	# tmp102,
	movss	DWORD PTR -12[rbp], xmm0	# x2, tmp102
# Test.c:7:     float x = x1 + x2;
	movss	xmm0, DWORD PTR -16[rbp]	# tmp104, x1
	addss	xmm0, DWORD PTR -12[rbp]	# x_4, x2
	movss	DWORD PTR -8[rbp], xmm0	# x, x_4
# Test.c:8:     int r = (uint32_t)x;
	movss	xmm0, DWORD PTR -8[rbp]	# tmp106, x
	cvttss2si	rax, xmm0	# tmp105, tmp106
# Test.c:8:     int r = (uint32_t)x;
	mov	DWORD PTR -4[rbp], eax	# r, _1
# Test.c:9:     return 0;
	mov	eax, 0	# _6,
# Test.c:10: }
	pop	rbp	#
	ret	
	.size	main, .-main
	.section	.rodata
	.align 4
.LC0:
	.long	1091987046
	.align 4
.LC1:
	.long	1083808154
	.ident	"GCC: (GNU) 14.2.1 20240910"
	.section	.note.GNU-stack,"",@progbits
