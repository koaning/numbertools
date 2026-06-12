import math
from pathlib import Path

import pytest

from numbertoolkit import phi_digits

# "1." followed by 10000 decimal digits (10001 significant digits). Exact by
# construction: (10**p + math.isqrt(5 * 10**(2*p))) // 2 == floor(phi * 10^p).
REFERENCE = (Path(__file__).parent / "data" / "phi_10000.txt").read_text().strip()
REFERENCE_DIGITS = REFERENCE.replace(".", "")


def test_small_values():
    assert phi_digits(1) == "1"
    assert phi_digits(2) == "16"
    assert phi_digits(5) == "16180"
    assert phi_digits(51) == "161803398874989484820458683436563811772030917980576"


def test_decimal_point():
    assert phi_digits(1, decimal_point=True) == "1"
    assert phi_digits(5, decimal_point=True) == "1.6180"


@pytest.mark.parametrize("n", [100, 1000, 9999, 10001])
def test_matches_reference(n):
    assert phi_digits(n) == REFERENCE_DIGITS[:n]


@pytest.mark.parametrize("n", [1, 2, 7, 100, 1234])
def test_prefix_consistency(n):
    longer = phi_digits(n + 137)
    assert longer.startswith(phi_digits(n))


@pytest.mark.parametrize("bad", [0, -5])
def test_rejects_nonpositive(bad):
    with pytest.raises(ValueError):
        phi_digits(bad)


@pytest.mark.parametrize("bad", ["10", 3.5, None])
def test_rejects_non_int(bad):
    with pytest.raises(TypeError):
        phi_digits(bad)


def isqrt_phi(digits: int) -> str:
    """phi via math.isqrt — an implementation independent of the Rust code."""
    p = digits + 14
    return str((10**p + math.isqrt(5 * 10 ** (2 * p))) // 2)[:digits]


def test_independent_isqrt_cross_check():
    assert phi_digits(1000) == isqrt_phi(1000)


def test_golden_ratio_identity():
    # phi^2 = phi + 1. With v = floor(phi * b), b = 10^(n-1), the truncation
    # error propagates as |v^2 - v*b - b^2| < sqrt(5)*b + 1 < 3*b.
    n = 500
    v = int(phi_digits(n))
    b = 10 ** (n - 1)
    assert abs(v * v - v * b - b * b) < 3 * b


@pytest.mark.slow
def test_large_n_completes():
    s = phi_digits(100_000)
    assert len(s) == 100_000
    assert s.startswith("161803398874989")
    assert s == phi_digits(100_137)[:100_000]
