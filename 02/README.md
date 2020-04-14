# Lessons

## 2's complement

Properties:

- (max-min) n bits signed number world, max=2^(n-1) - 1 and min=-2^(n-1)
- ⭐(convert) obtain -x code from x.
    - **For bare hand**: leave all trailing 0 keep first least significat 1 intact and flip all the remaining bits.
    - **For calulator**: flip all bits and add 1 to the result. 
     > Impl subtraction using this property.

My mindset for this:

The negative King is 10000.. = -2^n. His power will decrease by 1 point as we increase 1 point to his people.

# Project

## Adder

### Half-adder: add two bits

input has two bits, a and b, output is a 2-bit number, significant bit is carry and another is sum.

carry impl by And / sum impl by Xor

### Full-adder: add three bits

input has three bits, a and b and c, output is the same with half-adder

a b c | carry | sum
----- |  ---  | -
0 0 0 |  0    | 0
0 0 1 |  0    | 1
0 1 0 |  0    | 1
0 1 1 |  1    | 0
1 0 0 |  0    | 1
1 0 1 |  1    | 0
1 1 0 |  1    | 0
1 1 1 |  1    | 1

we already know how to add two bits in half-adder, here we just need to add the extra bit to the result of half-adder and Or the two carries produced by the the half-add

### Adder: add two n-bit number

cascade n full-adders, every full-adder produces a bit of result


## ALU

The essential part of ALU is the 6 control bits and control flow, all of them are already given.

What we need to do is simply put all blocks together.

- use Not to negate
- use Mux handle selections happening in zx / nx / zy / ny / no
- use Or16Way to set output status zr / ng


# Perspectives

## Another Adder
```python
def add(x, y):
    MASK = 0xFFFFFFFF
    res = x ^ y
    carry = ((x & y) << 1) & MASK
    while carry:
        res, carry = res ^ carry, ((res & carry) << 1) & MASK
    res &= MASK
    if res >= 2 ** 31:
        return res - 2 ** 32
    else:
        return res

def test_add():
    assert add(1, 2) == 3
    assert add(1, 0) == 1
    assert add(0, 0) == 0
    assert add(-1, 2) == 1
    assert add(-111, 110) == -1
    assert add(-3, 2) == -1
    assert add(-1, 0) == -1
    assert add(-111, 11) == -100
    assert add(2147483647, 0) == 2147483647
    assert add(2147483647, 1) == -2147483648 # overflow
    assert add(-2147483648, 0) == -2147483648
```

we can calculate carry in a batch



## Why Builtin chips are recommended when doing new project?
two reasons:
    
1. It is kind of unittest. If some bugs come up, we will know them root in current implementations, having no matter with previous chips we have built. This is the only way to fight against complexity.
2. HardwareSimulator will be more efficient to works with builtin chips.
