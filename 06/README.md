# Lessons

Assembler can be written by any high-level language

## Symbol resolution
- Variables: map to some address, the actual address values are insignificant
- Labels: assigned to specific instruction address

1. Address space reserved for instruction should be dynamic, at least larger?
2. One command may generate more than one variable, assembler needs to track them.
3. Assembler must consider various data types' requirements for number of register

# Project

My solution is line-based handling. It's simple and easyunderstood, but enough for Hack.

Done for now:
- Good for Hack asm file
- Nice error handling, having readable error message
- Support macro expand and it is easy to add more macros  
   ✔ `D=M[R0]`、 `M[i]=M[i] + 1`  
   ✔ `D;JGT @OUTPUT_FIRST`、 `0;JMP @INFINITE_LOOP`  
- Be able to handle large asm file (actually unnecessary early optimization)

TODO:
- Support expression like `D=M[i+3]`. One possible solution is to evaluate `i+3` in `SymbolTable`
