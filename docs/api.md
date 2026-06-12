# API reference

All digit functions return the first `n` significant digits as a raw digit
string, truncated (not rounded). The decimal point is omitted by default;
pass `decimal_point=True` to include it.

## `pi_digits`

```python
def pi_digits(n: int, *, decimal_point: bool = False) -> str
```

Return the first `n` significant digits of pi as a string.

```python
from numbertoolkit import pi_digits

pi_digits(1)                       # '3'
pi_digits(5)                       # '31415'
pi_digits(10)                      # '3141592653'
pi_digits(10, decimal_point=True)  # '3.141592653'
```

**Parameters**

- `n` — the number of significant digits to compute. Must be a positive
  integer; the count includes the leading `3`.
- `decimal_point` — keyword-only; include the decimal point after the first
  digit. Defaults to `False`.

**Returns**

A digit string `"31415..."` with `n` significant digits, or
`"3.1415..."` with `decimal_point=True`.

**Raises**

- `ValueError` — if `n < 1`
- `TypeError` — if `n` is not an integer

!!! note "Truncated, not rounded"

    Digits are truncated: `pi_digits(5)` returns `'31415'` even though the
    next digit is a 9. As a consequence, longer outputs always start with
    shorter ones: `pi_digits(100).startswith(pi_digits(10))` is `True`.

### Algorithm

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

## `e_digits`

```python
def e_digits(n: int, *, decimal_point: bool = False) -> str
```

Return the first `n` significant digits of Euler's number e as a string.

```python
from numbertoolkit import e_digits

e_digits(5)                       # '27182'
e_digits(10, decimal_point=True)  # '2.718281828'
```

Parameters, return value, and errors mirror `pi_digits`.

### Algorithm

Binary splitting over the factorial series

$$
e = \sum_{k=0}^{\infty} \frac{1}{k!}
$$

using the same exact-integer approach and 12-digit guard band as
`pi_digits`. The series converges superlinearly — roughly `log10(N!)` digits
after `N` terms — so a million digits needs only about 205,000 terms.

## `phi_digits`

```python
def phi_digits(n: int, *, decimal_point: bool = False) -> str
```

Return the first `n` significant digits of the golden ratio
\(\varphi = (1 + \sqrt{5}) / 2\) as a string.

```python
from numbertoolkit import phi_digits

phi_digits(5)                       # '16180'
phi_digits(10, decimal_point=True)  # '1.618033988'
```

Parameters, return value, and errors mirror `pi_digits`.

### Algorithm

No series is needed: the identity

$$
\lfloor \varphi \cdot 10^{p} \rfloor =
\left\lfloor \frac{10^{p} + \lfloor\sqrt{5 \cdot 10^{2p}}\rfloor}{2} \right\rfloor
$$

holds exactly because \(\sqrt{5} \cdot 10^{p}\) is irrational, so a single
exact integer floor square root produces every digit exactly.
