# Benchmarks

Computing pi digits with numbertoolkit versus [mpmath](https://mpmath.org),
measured on an Apple Silicon laptop:

| digits | numbertoolkit | mpmath | speedup vs mpmath |
|---:|---:|---:|---:|
| 10,000 | 0.0008s | 0.0052s | 6x |
| 100,000 | 0.0154s | 0.1926s | 13x |
| 1,000,000 | 0.2526s | 9.0297s | 36x |

The gap widens with digit count because numbertoolkit's binary-splitting
Chudnovsky implementation scales quasi-linearly, and the Rust extension
avoids Python-level overhead in the hot loop.

## Running the benchmarks yourself

The benchmark suite compares numbertoolkit against mpmath and a
stdlib-`decimal` baseline using Machin's formula, and cross-checks that all
implementations agree on the digits they produce:

```sh
make bench
# or directly:
uv run --group bench benchmarks/bench_pi.py
```

The Machin baseline is only run up to 5,000 digits since it scales
quadratically.

!!! warning "Benchmark release builds only"

    A debug build of the extension (`maturin develop` without `-r`) is
    10–50x slower. Always build in release mode before timing anything.
