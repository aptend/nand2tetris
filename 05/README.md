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
