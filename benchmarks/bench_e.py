"""Benchmark numbertoolkit.e_digits against other ways of computing e digits.

Run with:

    uv run --group bench benchmarks/bench_e.py

Compared implementations:
- numbertoolkit.e_digits (Rust, factorial series + binary splitting)
- mpmath (pure-Python arbitrary precision)
- stdlib integer term-by-term Taylor sum (naive O(n^2) baseline, small n only)

Sizes are benchmarked in ascending order on purpose: mpmath memoizes e at the
highest precision computed so far, so ascending order forces a fresh
computation at every size.
"""

import sys
import time

import mpmath

import numbertoolkit

sys.set_int_max_str_digits(0)

SIZES = [100, 1_000, 10_000, 100_000, 1_000_000]
TAYLOR_MAX_N = 5_000  # the term-by-term baseline is O(n^2); keep it tractable


def time_once(fn):
    start = time.perf_counter()
    result = fn()
    return result, time.perf_counter() - start


def mpmath_digits(n: int) -> str:
    mpmath.mp.dps = n
    return mpmath.nstr(mpmath.e, n).replace(".", "")


def taylor_digits(n: int) -> str:
    scale = 10 ** (n + 14)
    total = term = scale  # k = 0 term
    k = 1
    while term:
        term //= k
        total += term
        k += 1
    return str(total)


def fmt(seconds: float | None) -> str:
    return "—" if seconds is None else f"{seconds:.4f}s"


def main() -> None:
    rows = []
    for n in SIZES:
        ours, t_ours = time_once(lambda: numbertoolkit.e_digits(n))
        ref, t_mp = time_once(lambda: mpmath_digits(n))
        # compare all but the last digit: mpmath rounds, numbertoolkit truncates
        assert ours[: n - 1] == ref[: n - 1], f"digit mismatch at n={n}"

        t_taylor = None
        if n <= TAYLOR_MAX_N:
            taylor, t_taylor = time_once(lambda: taylor_digits(n))
            assert ours[: n - 1] == taylor[: n - 1], f"taylor mismatch at n={n}"

        rows.append((n, t_ours, t_mp, t_taylor))
        print(f"done n={n:,}", flush=True)

    print()
    print("| digits | numbertoolkit | mpmath | speedup vs mpmath | int Taylor |")
    print("|---:|---:|---:|---:|---:|")
    for n, t_ours, t_mp, t_taylor in rows:
        print(
            f"| {n:,} | {fmt(t_ours)} | {fmt(t_mp)} | {t_mp / t_ours:.0f}x | {fmt(t_taylor)} |"
        )


if __name__ == "__main__":
    main()
