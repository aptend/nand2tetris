// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/06/max/MaxM.asm

// M-macro version of the Max.asm

   D=M[0]         // D = first number
   D=D-M[R1]      // D = first number - second number
   @OUTPUT_FIRST
   D;JGT          // if D>0 (first is greater) goto output_first
   D=M[R1]        // D = second number
   @OUTPUT_D
   0;JMP          // goto output_d
(OUTPUT_FIRST)
   D=M[R0]        // D = first number
(OUTPUT_D)
   M[R2]=D        // M[2] = D (greatest number)
(INFINITE_LOOP)
   @INFINITE_LOOP
   0;JMP          // infinite loop
