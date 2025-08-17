@R2
M=0
@R1
D=M 
// value of @R1 now stored in D
(LOOP)
	@R1
	D=M
	@END
	D;JEQ

	@R0
	D=M
	@R2
	M=D+M

	@R1
	M=M-1

	@LOOP
	0;JMP
(END)
	@END
	0;JMP
