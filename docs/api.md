# API reference

## `pi_digits`

```python
def pi_digits(n: int) -> str
```

Return the first `n` significant digits of pi as a string.

```python
from numbertoolkit import pi_digits

pi_digits(1)   # '3'
pi_digits(5)   # '3.1415'
pi_digits(10)  # '3.141592653'
```

**Parameters**

- `n` — the number of significant digits to compute. Must be a positive
  integer; the count includes the leading `3`.

**Returns**

A string of the form `"3.1415..."` with `n` significant digits (or `"3"`
when `n == 1`).

**Raises**

- `ValueError` — if `n < 1`
- `TypeError` — if `n` is not an integer

!!! note "Truncated, not rounded"

    Digits are truncated: `pi_digits(5)` returns `'3.1415'` even though the
    next digit is a 9. As a consequence, longer outputs always start with
    shorter ones: `pi_digits(100).startswith(pi_digits(10))` is `True`.

## Algorithm

`pi_digits` implements the [Chudnovsky series](https://en.wikipedia.org/wiki/Chudnovsky_algorithm)
with binary splitting:

$$
\pi = \frac{426880\,\sqrt{10005}}{\displaystyle\sum_{k=0}^{\infty}
\frac{(-1)^k\,(6k)!\,(13591409 + 545140134\,k)}{(3k)!\,(k!)^3\,640320^{3k}}}
$$

All arithmetic is exact integer arithmetic scaled by a power of ten — the
square root is an exact integer floor square root, and no floating point is
involved anywhere. The series yields roughly 14.18 digits per term, and a
12-digit guard band absorbs truncation error from the discarded series tail,
so the output is exactly \(\lfloor \pi \cdot 10^{n-1} \rfloor\) rendered as
a string.

Binary splitting keeps the cost of combining series terms low, so the
computation scales quasi-linearly with `n` rather than quadratically.
Big-integer arithmetic is provided by the Rust
[malachite](https://crates.io/crates/malachite) crate.
