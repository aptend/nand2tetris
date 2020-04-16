# Lessons

## von Neumann machine
Stored Program -> amazing versatility

- Memory: data + instructions (stored program written by *machine language*)
- CPU: ALU + Registers + Control Unit
  - control unit is responsible for decoding the instruction, preparing to execute it, deciding what next to execute
  - Data register / Addressing register / PC register
- Input & Output
  - Memory mapping

## Hack

### Overview:

Memory: RAM & ROM

Three Registers: D / A / PC

Machine Language:
- A-instruction. 0vvv vvvv vvvv vvvv store 15-bit to A
- C-instruction. 111accccccdddjjj

Execute-Fetch cycle:

- Execute: A- or C-instruction?
- Fetch: if has jjj then set PC else PC += 1

Input & Output:

Outside logic
- Whenever a bit is changed in the screen’s memory map, a respective pixel is drawn on the physical screen
- Whenever a key is pressed, the respective code of this key appears in the keyboard map

# Project


## Memory & Computer
straight-forward

## CPU

### Decode instruction
```c
// decode the instruction
Or(a=instruction[15], b=false, out=cins);  // C-instruction
And(a=instruction[0], b=cins, out=j3);
And(a=instruction[1], b=cins, out=j2);
And(a=instruction[2], b=cins, out=j1);
And(a=instruction[3], b=cins, out=writeM); // d3, write to Memory if C-instruction
And(a=instruction[4], b=cins, out=dD);     // d2, write to DReg if C-instruction
And(a=instruction[5], b=cins, out=dA);     // d1, write to AReg if C-instruction
And(a=instruction[6], b=cins, out=c6);     // no
And(a=instruction[7], b=cins, out=c5);     // f
And(a=instruction[8], b=cins, out=c4);     // zy
And(a=instruction[9], b=cins, out=c3);     // ny
And(a=instruction[10], b=cins, out=c2);    // zx
And(a=instruction[11], b=cins, out=c1);    // nx
And(a=instruction[12], b=cins, out=sleM);  // feed ALU with M[A]
```

### Load value from ARegister
d1 | instructin mode | write to ARegister
--| -- | --
0 | 0 | 1
1 | 0 | 1
1 | 1 | 1 
0 | 1 | 0

`loadA = (d1 & imode) or not imode`

### Jump cases

The hard part for me is `f(zr, ng, j-bits) -> pc_load`

I put my solution as following:

```python
0 0 out > 0      101 001 011 | 111
0 1 out < 0      101 100 110 | 111
1 0 out = 0      010 011 110 | 111

- (zr & j2) covers 3 cases: 10(010|011|110)
- (not zr) and (j1 & j3) covers 2 cases: 00101、01101
- (not zr) and (j1 ^ j3 and ng ^ j3) covers 4 cases: 00(001|011)、01(100|110)
- (j1 & j2 & j3) covers left cases(some duplicated cases)

jump = (j1 & j2 & j3) or (zr & j2) or not zr and (j1 & j3) or (j1 ^ j3 and ng ^ j3)
```
