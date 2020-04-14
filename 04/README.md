# Lessons

## Machine Language:
- What's the operation?
- What's the operands and where to find them?
- How do we know what to do next? **control flow**

> Design cost-performance tradeoff:
>
> Support larger or more sophisticated data types will cost more money and take more time to complete.


### Operations
common:
- Arithmetic op: add sub...
- Logical op: and or...
- Control op: goto if x goto...
  
difference:
- Richness of ops: division?
- Data types: withd, floats

### Operands

Access quickly using Memory Hierarchy

CPU register -> cache -> main memory -> disk

data register: `Add R1, R2`
address register: `Store R2, @A`

we can get four addressing modes:
- Register: `Add R1, R2`
- Direct: `Add R1, M[200]`
- Indirect: `Add R1, @A`
- Immediate: `Add 73, R1`

### Control Flow

- sequence
- jump -> to a location name
- conditional jump
