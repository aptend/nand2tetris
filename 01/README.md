## Not & Not16

Not(a) = Nand(a, a)

---

## And & And16

And(a, b) = Not(Nand(a, b))

---

## Or && Or16

not-a and not-b = not-(a or b), so not-(not-a and not-b) = a or b

---

## Or8Way

`in[8].fold(0, |a, b| a or b);`

---

## Xor

xor(a, b) = (not-a and b) or (not-b and a)
