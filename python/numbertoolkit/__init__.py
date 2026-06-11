"""Fast number theory utilities backed by Rust."""

from numbertoolkit._core import pi_digits
from numbertoolkit._core import sqrt_digits as _sqrt_digits

__all__ = ["pi_digits", "sqrt_digits"]


def sqrt_digits(d: int, n: int, *, decimal_point: bool = True) -> str:
    """First `n` significant digits of sqrt(d), truncated (not rounded).

    `sqrt_digits(2, 5) == "1.4142"`. Pass `decimal_point=False` to drop the
    radix point and return only the digit string: `sqrt_digits(2, 5,
    decimal_point=False) == "14142"`.
    """
    s = _sqrt_digits(d, n)
    if not decimal_point:
        # Exactly one "." is ever present; count=1 stops the scan at it instead
        # of walking the whole (potentially million-char) string for more.
        return s.replace(".", "", 1)
    return s
