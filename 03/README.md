# Lessons

- combinational chips: functional, no state

    Once given the input in one time cycle, the output can be determined in the same time cycle.

- sequential chips: be able to maintain state(register) or operate on state(counter) 
    
    **consist of a layer of DFFs sandwithced between optional combinational logic layers**
    
    DFF introduces an **inherent time delay**: the output at time *t* doesn't depend on itself, but rather on the output at time *t-1*. It is safe to form feedback loop in sequential chips


Of course, DFF can be made by combinational chips with loops. However, it is recommended to have separated mindsets for combinational and sequential chips. The combinational can't be loop connected and their outputs depend on inputs in the current time cycle. The sequential can be loop connected and their outputs depend on inputs in the previous time cycle.


## Concepts

### The Clock

cycle: tick low 0 -> tock high 1

signal is simultaneously broadcast to every sequential chip throughout the computer platform

### Flip-Flops

⭐ the most elementry sequential element

DFF, `out(t) = in(t-1)`

⭐ DFF simply outputs the input value from the previous time unit.

### Registers

registers holds their outputs. `out(t) = out(t-1)`, the output doesn't change as tick-tock going on.

```shell
                |
                | load
in              v
------------>+--+--+      +-----+            out
             | Mux +----> + DFF + ---------------> 
          -->+-----+      +-----+    |
          |                          |
          ----------------------------
```

This design is able to remember one bit. We call it Binary cell(bit).

Function: `if load(t-1) then out(t)=in(t-1) else out(t)=out(t-1)`

- `width`: the number of bits that a register holds, 16,32, or 64
- `words`: the multi-bit contents of registers are referred to

### Memories

stack n registers to form RAM.

input:
- in(word)
- address
- load bit(0 for read, 1 for write)

output:
- out(word)

### Counters
`if inc(t-1) then out(t) = out(t-1) + c`, where c is typically 1

`program counter: pc register`

Extra funtion:

- loadable
- resettable

There are 3 control bits: inc, reset, load


⭐ Time Delay

With the help of the following image, I understand a little about the meaning of `t` and expression of `if inc(t-1) then out(t) = out(t-1)` blabla...

![GzfRkq.png](https://s1.ax1x.com/2020/04/14/GzfRkq.png)

### Time matters

How to synchronize the overall computer archtecture?

For instance, the inputs of ALU, x+y, where x is the value of a nearby register, y is the value of a remote RAM register. ALU will generate garbage until y is load to a nearby register.

All we have to do is ensure, when we build the computer’s clock, that
the length of the clock cycle will be slightly longer that the time it takes a bit to travel
the longest distance from one chip in the architecture to another. 


# Projects

## DFF

- Provided. 
- All DFFs are connected to the same master clock.

## Bit & Register

Impl is straight-forward.

## RAM8

use DMux8Way to dispatch `load` signal, and use Mux8Way16 to select final output.

## RAM64

address[3..5] decides which RAM8 to access and address[0..2] decides which register to access.

## Counter


`reset` has the highest priority, following by `load`, the lowest is `inc`.

So I'd like to impl this in a reversed order.

```c
Inc16(in=feedback, out=inc1);
Mux16(a=feedback, b=inc1, sel=inc, out=doneinc);
Mux16(a=doneinc, b=in, sel=load, out=doneload);
Mux16(a=doneload, b=false, sel=reset, out=donereset);
// introduce DFF to enable loop connection
Register(in=donereset, load=true, out=feedback);
Or16(a=feedback, b=false, out=out);
```

As we use feedback during handing `inc` condition, we can set register's `load` always `true`. Of course, we can also enable it only when Or(inc, reset, load) is true, which means update operation happens.
