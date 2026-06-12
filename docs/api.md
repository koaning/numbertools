# API reference

The digit functions return the first `n` significant digits as a string,
truncated (not rounded). A keyword-only `decimal_point` flag controls whether
the decimal point is included — the constant functions (`pi_digits`,
`e_digits`, `phi_digits`) omit it by default, `sqrt_digits` includes it by
default.

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

## `sqrt_digits`

```python
def sqrt_digits(d: int, n: int, *, decimal_point: bool = True) -> str
```

Return the first `n` significant digits of the square root of a positive
integer `d` as a string.

```python
from numbertoolkit import sqrt_digits

sqrt_digits(2, 5)                        # '1.4142'
sqrt_digits(2, 10)                       # '1.414213562'
sqrt_digits(2, 5, decimal_point=False)   # '14142'
sqrt_digits(200, 6)                      # '14.1421'
sqrt_digits(4, 5)                        # '2.0000'
```

**Parameters**

- `d` — the radicand. Must be a positive integer.
- `n` — the number of significant digits to compute. Must be a positive
  integer; the count includes every digit of the integer part.
- `decimal_point` — keyword-only; include the decimal point after the
  integer part. Defaults to `True`.

**Returns**

A string like `"1.4142..."` with `n` significant digits, or the raw digit
stream `"14142..."` with `decimal_point=False`. Perfect squares pad with
trailing zeros: `sqrt_digits(4, 5)` is `'2.0000'`.

**Raises**

- `ValueError` — if `d < 1` or `n < 1`
- `TypeError` — if `d` or `n` is not an integer

!!! note "Decimal point included by default"

    Unlike the constant functions, `sqrt_digits` includes the decimal point
    by default: the integer part of \(\sqrt{d}\) isn't a single known digit
    (`sqrt_digits(200, 6)` starts with `14`), so the raw digit stream alone
    is ambiguous.

### Algorithm

No series is needed: the identity

$$
\lfloor \sqrt{d} \cdot 10^{p} \rfloor =
\lfloor \sqrt{d \cdot 10^{2p}} \rfloor
$$

holds exactly, so a single exact integer floor square root produces every
digit. Because the floor square root is exact, no guard digits are required
— `p = n` already yields the exact truncated prefix. No floating point and
no division are involved.

## `is_prime`

```python
def is_prime(n: int) -> bool
```

Return whether `n` is a prime number.

```python
from numbertoolkit import is_prime

is_prime(17)    # True
is_prime(1)     # False
is_prime(-7)    # False
```

**Parameters**

- `n` — the integer to test. Anything below 2 (including negatives, 0 and
  1) is not prime.

**Returns**

`True` if `n` is prime, `False` otherwise.

**Raises**

- `TypeError` — if `n` is not an integer

### Algorithm

Trial division: after checking 2, only odd divisors up to \(\sqrt{n}\) are
tried. This is exact for the full 64-bit range and fast for moderate inputs;
it is not intended for cryptographic-size numbers.

## `first_n_primes`

```python
def first_n_primes(n: int) -> list[int]
```

Return the first `n` prime numbers in ascending order.

```python
from numbertoolkit import first_n_primes

first_n_primes(5)    # [2, 3, 5, 7, 11]
first_n_primes(0)    # []
```

**Parameters**

- `n` — how many primes to return. Must be a non-negative integer.

**Returns**

A list of the first `n` primes, starting from 2.

**Raises**

- `ValueError` — if `n < 0`
- `TypeError` — if `n` is not an integer

### Algorithm

Candidates are tested in ascending order with the same trial division as
`is_prime` until `n` primes have been collected.
