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


## Memory
straight-forward

## CPU

d1 | instructin mode | write to ARegister
--| -- | --
0 | 0 | 1
1 | 0 | 1
1 | 1 | 1 
0 | 1 | 0

The hard part for me is `f(zr, ng, j-bits) -> pc_load`

I put my solution as following:

```python
0 0 out > 0      101 001 011 | 111
0 1 out < 0      101 100 110 | 111  not zr and (j1 & j3) or (j1 ^ j3 and ng ^ j3)
1 0 out = 0      010 011 110 | 111  zr & j2
jump_anyway = (j1 & j2 & j3)
jump = jump_anyway or (zr & j2) or not zr and (j1 & j3) or (j1 ^ j3 and ng ^ j3)
```
