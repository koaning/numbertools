"""Fast number theory utilities backed by Rust."""

from numbertoolkit import _core

__all__ = ["e_digits", "phi_digits", "pi_digits"]


def _with_point(digits: str) -> str:
    return f"{digits[0]}.{digits[1:]}" if len(digits) > 1 else digits


def pi_digits(n: int, *, decimal_point: bool = False) -> str:
    """First `n` significant digits of pi, truncated: `pi_digits(5) == "31415"`.

    Pass `decimal_point=True` to include the decimal point: `"3.1415"`.
    """
    digits = _core.pi_digits(n)
    return _with_point(digits) if decimal_point else digits


def e_digits(n: int, *, decimal_point: bool = False) -> str:
    """First `n` significant digits of e, truncated: `e_digits(5) == "27182"`.

    Pass `decimal_point=True` to include the decimal point: `"2.7182"`.
    """
    digits = _core.e_digits(n)
    return _with_point(digits) if decimal_point else digits


def phi_digits(n: int, *, decimal_point: bool = False) -> str:
    """First `n` significant digits of the golden ratio, truncated:
    `phi_digits(5) == "16180"`.

    Pass `decimal_point=True` to include the decimal point: `"1.6180"`.
    """
    digits = _core.phi_digits(n)
    return _with_point(digits) if decimal_point else digits
