"""Benchmark numbertools.pi_digits against other ways of computing pi digits.

Run with:

    uv run --group bench benchmarks/bench_pi.py

Compared implementations:
- numbertools.pi_digits (Rust, Chudnovsky + binary splitting)
- mpmath (pure-Python arbitrary precision, also Chudnovsky-based)
- stdlib decimal with Machin's formula (naive O(n^2) baseline, small n only)

Sizes are benchmarked in ascending order on purpose: mpmath memoizes pi at the
highest precision computed so far, so ascending order forces a fresh
computation at every size.
"""

import time
from decimal import Decimal, getcontext

import mpmath

import numbertools

SIZES = [100, 1_000, 10_000, 100_000, 1_000_000]
DECIMAL_MAX_N = 5_000  # the Machin baseline is O(n^2); keep it tractable


def time_once(fn):
    start = time.perf_counter()
    result = fn()
    return result, time.perf_counter() - start


def mpmath_digits(n: int) -> str:
    mpmath.mp.dps = n
    return mpmath.nstr(mpmath.pi, n)


def machin_decimal_digits(n: int) -> str:
    getcontext().prec = n + 20
    threshold = Decimal(1).scaleb(-(n + 15))

    def arctan_inv(x: int) -> Decimal:
        total = term = Decimal(1) / x
        x2 = x * x
        k, sign = 1, 1
        while term > threshold:
            term /= x2
            k += 2
            sign = -sign
            total += sign * term / k
        return total

    return str(16 * arctan_inv(5) - 4 * arctan_inv(239))


def fmt(seconds: float | None) -> str:
    return "—" if seconds is None else f"{seconds:.4f}s"


def main() -> None:
    rows = []
    for n in SIZES:
        ours, t_ours = time_once(lambda: numbertools.pi_digits(n))
        ref, t_mp = time_once(lambda: mpmath_digits(n))
        # compare all but the last digit: mpmath rounds, numbertools truncates
        assert ours[: n - 1] == ref[: n - 1], f"digit mismatch at n={n}"

        t_dec = None
        if n <= DECIMAL_MAX_N:
            dec, t_dec = time_once(lambda: machin_decimal_digits(n))
            assert ours[: n - 1] == dec[: n - 1], f"decimal mismatch at n={n}"

        rows.append((n, t_ours, t_mp, t_dec))
        print(f"done n={n:,}", flush=True)

    print()
    print("| digits | numbertools | mpmath | speedup vs mpmath | decimal (Machin) |")
    print("|---:|---:|---:|---:|---:|")
    for n, t_ours, t_mp, t_dec in rows:
        print(
            f"| {n:,} | {fmt(t_ours)} | {fmt(t_mp)} | {t_mp / t_ours:.0f}x | {fmt(t_dec)} |"
        )


if __name__ == "__main__":
    main()
