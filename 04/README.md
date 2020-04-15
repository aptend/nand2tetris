# Lessons

## Machine Language:
⭐
- What's the operation?   ------------------------------|
- What's the operands and where to find them? ---+---`an instruction`
- How do we know what to do next? **control flow**

> Design cost-performance tradeoff:
>
> Support larger or more sophisticated data types will cost more money and take more time to complete.


### Operations
common:
- Arithmetic op: add, sub...
- Logical op: and, or...
- Control op: goto, if x goto...
  
difference:
- Richness of ops: division?
- Data types: withd, floats

### Operands

Access quickly using Memory Hierarchy

CPU register -> cache -> main memory -> disk

⭐
we can get four addressing modes:
- Register: `Add R2, R1, R3` // R2 <- R1 + R3
- Immediate: `LOADI R1, 67` // R1 <- 67
- Direct: `Load R1, 67` // R1 <- M[67]
- Indirect: `LOAD* R2, R1` // R2 <- M[R1]
    
    In C language， `*n` means the value of `M[n]`
    ```c
    // translation of x = foo[j] or x = *(foo+j)
    ADD R1, foo, j // R1 <- foo + j
    LOAD* R2, R1 // R2 <- M[R1]
    STR R2, x // x <- R2
    ```



### Control Flow

- sequence
- jump -> to a location name
- conditional jump

## Hack

### Overview

- Two memory address spaces (15-bit): *instruction memory(ROM>)* and *data memory(RAM)*
- Two 16-bit register: *D* for store data values and *A* for data and address. label     *M* means the value of Memory[A]
    > instruction memory width is 16, and space is 15-bit, it is impossible to store both op and address in only one instruction. Is this means no direct address in Hack?

### A-Instruction

`@value`: store a value to A register

`0xxx xxxx xxxx xxxx` 

1. the only way to enter a constant to Hack
2. Specify the memory address where the next C-instruction operates on.
3. Sets the instruction address for a subsequent jump instruction


### C-Instruction

`dest=comp;jump`
```
1 1 1 a  c1 c2 c3 c4  c5 c6 d1 d2  d3 j1 j2 j3
- --- ---------------------- --------- --------
C unused      comp             dest      jump
```

#### comp

`a`: Where to find the operands?

`c1~c6`: What to do? Map the six controls of ALU

```
0, 1, -1, D, A, !D, !A, -D, -A, D+1, A+1, D-1, A-1, D+A, D-A, A-D, D&A, D|A
             M,     !M,     -M,      M+1,      M-1, D+M, D-M, M-D, D&M, D|M
```

#### dest

```
null, M, D, MD, A, AM, AD, AMD
0   no store
001 Memmory[A]
010 D register
011 M[A] and D
100 A register
101 A and M[A]
...
```


#### jump

```
null, JGT, JEQ, JGE, JLT, JNE, JLE, JMP
no    >0    =0  >=0   <   !=    <=  jump anyway
```

#### examples

```c
// increment the value of M[7] by 1 and also copy the out to D register
0000 0000 0000 0111 // @7
1111 1101 1101 1000 // MD=M+1

// if M[3] = 5 then goto 100 else goto 200
@3
D=M   // D=M[3]
@5
D=D-A // D=D-5
@100
D;JEQ
@200
0;JMP


// Adds 1+...+100.
    @i // i refers to some mem. location.
    M=1 // i=1
    @sum // sum refers to some mem. location.
    M=0 // sum=0
(LOOP)
    @i
    D=M // D=i
    @100
    D=D-A // D=i-100
    @END
    D;JGT // If (i-100)>0 goto END
    @i
    D=M // D=i
    @sum
    M=D+M // sum=sum+i
    @i
    M=M+1 // i=i+1
    @LOOP
    0;JMP // Goto LOOP
(END)
    @END
    0;JMP // Infinite loop
```

### Symbols

#### Predefined
- registers: R0 ~ R15 <-> 0x0000 ~ 0x000f
- pointers: SP, LCL, ARG, THIS, THAT <-> 0x0000, 0x0004
- IO pointers: SCREEN <-> 0x4000, KEYBOARD <-> 0x6000

#### Label symbols
- User-defined symbols, which serve to label destinations of jump commands.

- declared by '(Xxx)', refer to the instruction memory location holding the next command in the program.

- Access globally

#### Variable symbols
- Any symbols that are not covered by predefined and label. Every variable is a unique memory address starting 16(0x0010).


### Inupt/Output Handling

- Memory mapping
- Synchronized via continuous refresh

screen size: 256 rows, 512 pixels, mapping zigzag, starting from top-left
```c
@SCREEN
M=1 // blacken left most pixel
M=3 // blacken left most 2 pixels
```

keyboard: whenever a key is pressed, its 16-bit ASCII code appears in 0x6000
```c
@KBD
D=M // load key value to D register
```


# Project

## Mult

1. clear R2
2. let R0 be the loop indicator, subtract it until zero.
3. accumulate R1 to R2


## Fill Screen

1. screen has 8192 words, store it at R0 as loop indicator
2. read KBD, if any key is pressed, then set R2 by black bucket(-1), else by white bucket(0)
3. read R0, check to break loop
4. store `to_fill_addr = SCREEN + R0-1` at R1
5. read R2
6. fill `to_fill_addr` by R2 bucket
7. goto 3
