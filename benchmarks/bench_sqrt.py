"""Benchmark numbertoolkit.sqrt_digits against other ways of computing sqrt digits.

Run with:

    uv run --group bench benchmarks/bench_sqrt.py

Compared implementations:
- numbertoolkit.sqrt_digits (Rust, exact integer floor_sqrt)
- mpmath (pure-Python arbitrary precision)
- stdlib decimal with Newton's method (g <- (g + d/g) / 2)

The radicand defaults to 2 (sqrt(2)); pass another integer as the first CLI
argument to benchmark a different root, e.g. `... bench_sqrt.py 3`.
"""

import sys
import time
from decimal import Decimal, getcontext

import mpmath

import numbertoolkit

SIZES = [100, 1_000, 10_000, 100_000, 1_000_000]


def time_once(fn):
    start = time.perf_counter()
    result = fn()
    return result, time.perf_counter() - start


def mpmath_sqrt_digits(d: int, n: int) -> str:
    mpmath.mp.dps = n
    return mpmath.nstr(mpmath.sqrt(d), n)


def newton_decimal_digits(d: int, n: int) -> str:
    """sqrt(d) via Newton's method on the decimal module. Converges from above
    and monotonically decreasing (seed g_0 = d >= sqrt(d) for d >= 1)."""
    getcontext().prec = n + 20
    x = Decimal(d)
    prev = x
    guess = (prev + x / prev) / 2
    while guess < prev:
        prev = guess
        guess = (guess + x / guess) / 2
    return str(prev)


def fmt(seconds: float | None) -> str:
    return "—" if seconds is None else f"{seconds:.4f}s"


def main() -> None:
    d = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    print(f"Benchmarking sqrt({d})\n")

    rows = []
    for n in SIZES:
        ours, t_ours = time_once(lambda: numbertoolkit.sqrt_digits(d, n))
        ref, t_mp = time_once(lambda: mpmath_sqrt_digits(d, n))
        # compare all but the last digit: mpmath rounds, numbertoolkit truncates
        assert ours[: n - 1] == ref[: n - 1], f"digit mismatch at n={n}"

        dec, t_dec = time_once(lambda: newton_decimal_digits(d, n))
        assert ours[: n - 1] == dec[: n - 1], f"decimal mismatch at n={n}"

        rows.append((n, t_ours, t_mp, t_dec))
        print(f"done n={n:,}", flush=True)

    print()
    print("| digits | numbertoolkit | mpmath | speedup vs mpmath | decimal (Newton) |")
    print("|---:|---:|---:|---:|---:|")
    for n, t_ours, t_mp, t_dec in rows:
        print(
            f"| {n:,} | {fmt(t_ours)} | {fmt(t_mp)} | {t_mp / t_ours:.0f}x | {fmt(t_dec)} |"
        )


if __name__ == "__main__":
    main()
