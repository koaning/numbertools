from decimal import Decimal, getcontext

import pytest

from numbertoolkit import sqrt_digits

# Known truncated expansions (50 decimal digits, 51 significant).
SQRT2 = "1.41421356237309504880168872420969807856967187537694"
SQRT3 = "1.73205080756887729352744634150587236694280525381038"


def test_small_values():
    assert sqrt_digits(2, 1) == "1"
    assert sqrt_digits(2, 5) == "1.4142"
    assert sqrt_digits(3, 5) == "1.7320"
    assert sqrt_digits(2, 51) == SQRT2
    assert sqrt_digits(3, 51) == SQRT3


@pytest.mark.parametrize("d", [2, 3, 5, 7, 200])
@pytest.mark.parametrize("n", [1, 2, 7, 100, 1234])
def test_prefix_consistency(d, n):
    longer = sqrt_digits(d, n + 137)
    assert longer.startswith(sqrt_digits(d, n))


def test_decimal_point_option():
    assert sqrt_digits(2, 5, decimal_point=False) == "14142"
    assert sqrt_digits(3, 5, decimal_point=False) == "17320"
    assert sqrt_digits(2, 1, decimal_point=False) == "1"
    assert sqrt_digits(200, 6, decimal_point=False) == "141421"
    # Default keeps the point.
    assert sqrt_digits(2, 5) == "1.4142"


def test_perfect_square():
    assert sqrt_digits(4, 5) == "2.0000"
    assert sqrt_digits(9, 3) == "3.00"


def test_multi_digit_integer_part():
    # sqrt(200) = 14.14213562...
    assert sqrt_digits(200, 2) == "14"
    assert sqrt_digits(200, 6) == "14.1421"


@pytest.mark.parametrize("bad", [0, -1])
def test_rejects_nonpositive_d(bad):
    with pytest.raises(ValueError):
        sqrt_digits(bad, 5)


@pytest.mark.parametrize("bad", [0, -5])
def test_rejects_nonpositive_n(bad):
    with pytest.raises(ValueError):
        sqrt_digits(2, bad)


@pytest.mark.parametrize("bad", ["2", 3.5, None])
def test_rejects_non_int(bad):
    with pytest.raises(TypeError):
        sqrt_digits(bad, 5)
    with pytest.raises(TypeError):
        sqrt_digits(2, bad)


def decimal_sqrt(d: int, n: int) -> str:
    """sqrt(d) to n significant digits, truncated, via Newton's method on the
    decimal module — independent of malachite and of any library sqrt().

    Newton iteration g_{k+1} = (g_k + d/g_k) / 2 converges to sqrt(d) from
    above and monotonically decreasing (seed g_0 = d >= sqrt(d) for d >= 1), so
    we stop once it stops decreasing and use the last value still >= sqrt(d).
    Extra guard precision keeps the truncated n-digit prefix exact.
    """
    getcontext().prec = n + 25
    x = Decimal(d)
    prev = x
    guess = (prev + x / prev) / 2
    while guess < prev:
        prev = guess
        guess = (guess + x / guess) / 2
    s = str(prev)
    int_part, _, frac = s.partition(".")
    int_len = len(int_part)
    digits = (int_part + frac)[:n]
    if n <= int_len:
        return digits
    return f"{digits[:int_len]}.{digits[int_len:]}"


@pytest.mark.slow
@pytest.mark.parametrize("d", [2, 3, 200])
def test_independent_decimal_cross_check(d):
    assert sqrt_digits(d, 1000) == decimal_sqrt(d, 1000)


@pytest.mark.slow
def test_large_n_completes():
    s = sqrt_digits(2, 100_000)
    assert len(s) == 100_001
    assert s.startswith("1.41421356237309")
    assert s == sqrt_digits(2, 100_137)[:100_001]
