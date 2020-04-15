// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
    @R2
    M=0 // clear R2
(LOOP)
    @R0
    D=M   // store D first, because M and jump can't be evaluated at the same time
    @END
    D;JEQ // if M[R0] == 0, break the loop
    @R0
    M=D-1 // M[R0] -= 1
    @R1
    D=M // D = M[R1]
    @R2
    M=M+D // M[R2] += D
    @LOOP
    0;JMP
(END)
    @END
    0;JMP // infinite loop
