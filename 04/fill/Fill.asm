// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


(READ)
    @8192 // screen maps 8192 16-bit totally
    D=A
    @R0
    M=D  // store 8192 to R0

    @KBD  // read key, do blacken or lighten
    D=M
    @SETBLACK
    D;JGT
    @SETLIGHT
    0;JMP

(SETBLACK)
    @R2
    M=-1
    @FILL
    0;JMP

(SETLIGHT)
    @R2
    M=0
(FILL)
(LOOP)
    @R0
    D=M // read r0
    @READ
    D;JLT // complete, jump to read
    @R0
    MD=D-1
    @SCREEN
    D=D+A  // calculate which word to fill and store it at R1
    @R1
    M=D
    @R2 // read color
    D=M
    @R1
    A=M
    M=D // fill it
    @LOOP
    0;JMP
