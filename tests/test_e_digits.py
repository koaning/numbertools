from pathlib import Path

import pytest

from numbertoolkit import e_digits

# "2." followed by 10000 decimal digits (10001 significant digits), generated
# with mpmath at higher precision and truncated.
REFERENCE = (Path(__file__).parent / "data" / "e_10000.txt").read_text().strip()
REFERENCE_DIGITS = REFERENCE.replace(".", "")


def test_small_values():
    assert e_digits(1) == "2"
    assert e_digits(2) == "27"
    assert e_digits(5) == "27182"
    assert e_digits(51) == "271828182845904523536028747135266249775724709369995"


def test_decimal_point():
    assert e_digits(1, decimal_point=True) == "2"
    assert e_digits(5, decimal_point=True) == "2.7182"


@pytest.mark.parametrize("n", [100, 1000, 9999, 10001])
def test_matches_reference(n):
    assert e_digits(n) == REFERENCE_DIGITS[:n]


@pytest.mark.parametrize("n", [1, 2, 7, 100, 1234])
def test_prefix_consistency(n):
    longer = e_digits(n + 137)
    assert longer.startswith(e_digits(n))


@pytest.mark.parametrize("bad", [0, -5])
def test_rejects_nonpositive(bad):
    with pytest.raises(ValueError):
        e_digits(bad)


@pytest.mark.parametrize("bad", ["10", 3.5, None])
def test_rejects_non_int(bad):
    with pytest.raises(TypeError):
        e_digits(bad)


def taylor_e(digits: int) -> str:
    """e via term-by-term summation of the factorial series with stdlib
    integers only — an algorithm and implementation independent of both the
    Rust code and the reference file."""
    scale = 10 ** (digits + 14)
    total = term = scale  # k = 0 term
    k = 1
    while term:
        term //= k
        total += term
        k += 1
    return str(total)[:digits]


@pytest.mark.slow
def test_independent_taylor_cross_check():
    assert e_digits(1000) == taylor_e(1000)


@pytest.mark.slow
def test_large_n_completes():
    s = e_digits(100_000)
    assert len(s) == 100_000
    assert s.startswith("271828182845904")
    assert s == e_digits(100_137)[:100_000]
