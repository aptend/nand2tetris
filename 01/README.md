## Not & Not16

Not(a) = Nand(a, a)


## And & And16

And(a, b) = Not(Nand(a, b))


## Or && Or16

not-a and not-b = not-(a or b), so not-(not-a and not-b) = a or b

## Or8Way

`in[8].fold(0, |a, b| a or b);`


## Xor

xor(a, b) = (not-a and b) or (not-b and a)


## Mux & Mux16

I'd like to call it selector.

General solution: `Or` every row with value 1, no fancy stuff.

Better solution: `x and 1` means `x` is selected and `x and 0` means `x` is deprecated. 

So we can do `(a and not-sel) or (b and sel)`.

Mux teaches us how to eliminate `if expression`


## Mux4Way16 & Mux8Way16

It is like a horse race game. First, we use sel[0] to select the winner from group(a, b) and group(c, d), then, we use sel[1] to select the final winner from them.


## DMux

I'd like to call it dispatcher

Do the same thing we did in Mux to impl DMux.

And we run a relay race in a binary tree, passing the input to a leaf.
