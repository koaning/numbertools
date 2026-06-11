from decimal import Decimal, getcontext
from pathlib import Path

import pytest

from numbertools import pi_digits

# "3." followed by 10000 decimal digits (10001 significant digits), generated
# with mpmath at higher precision and truncated.
REFERENCE = (Path(__file__).parent / "data" / "pi_10000.txt").read_text().strip()


def test_small_values():
    assert pi_digits(1) == "3"
    assert pi_digits(2) == "3.1"
    assert pi_digits(5) == "3.1415"
    assert pi_digits(51) == "3.14159265358979323846264338327950288419716939937510"


@pytest.mark.parametrize("n", [100, 1000, 9999, 10001])
def test_matches_reference(n):
    assert pi_digits(n) == REFERENCE[: n + 1]


def test_thousandth_decimal_digit():
    # The 1000th digit after the decimal point of pi is 9.
    assert pi_digits(1001)[-1] == "9" == REFERENCE[1001]


@pytest.mark.parametrize("n", [1, 2, 7, 100, 1234])
def test_prefix_consistency(n):
    longer = pi_digits(n + 137)
    assert longer.startswith(pi_digits(n))


@pytest.mark.parametrize("bad", [0, -5])
def test_rejects_nonpositive(bad):
    with pytest.raises(ValueError):
        pi_digits(bad)


@pytest.mark.parametrize("bad", ["10", 3.5, None])
def test_rejects_non_int(bad):
    with pytest.raises(TypeError):
        pi_digits(bad)


def machin_pi(digits: int) -> str:
    """pi via Machin's formula with the decimal module — an algorithm and
    implementation independent of both the Rust code and the reference file."""
    getcontext().prec = digits + 20
    threshold = Decimal(1).scaleb(-(digits + 15))

    def arctan_inv(x: int) -> Decimal:
        total = term = Decimal(1) / x
        x2 = x * x
        n, sign = 1, 1
        while term > threshold:
            term /= x2
            n += 2
            sign = -sign
            total += sign * term / n
        return total

    pi = 16 * arctan_inv(5) - 4 * arctan_inv(239)
    return str(pi)[: digits + 1]


@pytest.mark.slow
def test_independent_machin_cross_check():
    assert pi_digits(1000) == machin_pi(1000)


@pytest.mark.slow
def test_large_n_completes():
    s = pi_digits(100_000)
    assert len(s) == 100_001
    assert s.startswith("3.14159265358979")
    assert s == pi_digits(100_137)[:100_001]
