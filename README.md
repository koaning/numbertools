# numbertoolkit

Fast number theory utilities for Python, backed by Rust.

```python
import numbertoolkit

numbertoolkit.pi_digits(10)
# '3141592653'

numbertoolkit.pi_digits(10, decimal_point=True)
# '3.141592653'
```

## Functions

- `pi_digits`, `e_digits`, `phi_digits` — first `n` significant digits of
  pi, e, and the golden ratio
- `sqrt_digits` — first `n` significant digits of the square root of any
  positive integer
- `is_prime` — primality check
- `first_n_primes` — the first `n` primes in ascending order

Digit functions return truncated (not rounded) digit strings, computed with
exact integer arithmetic in Rust — fast well into the millions of digits.

## Documentation

Full docs live at [koaning.github.io/numbertools](https://koaning.github.io/numbertools/),
built with [Zensical](https://zensical.org) from the `docs/` directory. To
preview locally:

```sh
make docs    # live-reloading preview at http://localhost:8000
```

## Demo

An interactive [marimo](https://marimo.io) notebook demoing the package:

```sh
uv run marimo edit demo.py
```

## Benchmarks

Compare against mpmath and stdlib baselines:

```sh
uv run --group bench benchmarks/bench_pi.py
uv run --group bench benchmarks/bench_e.py
uv run --group bench benchmarks/bench_sqrt.py
```

On an Apple Silicon laptop:

| digits | numbertoolkit | mpmath | speedup vs mpmath |
|---:|---:|---:|---:|
| 10,000 | 0.0008s | 0.0052s | 6x |
| 100,000 | 0.0154s | 0.1926s | 13x |
| 1,000,000 | 0.2526s | 9.0297s | 36x |

## Development

Requires [Rust](https://rustup.rs) and [uv](https://docs.astral.sh/uv/).

```sh
make install                   # uv sync: build the extension and set up .venv
make test                      # cargo test + pytest
make bench                     # run the benchmark suite
uvx maturin develop --uv -r    # fast rebuild loop (release mode)
```

Note: `maturin develop` without `-r` produces a debug build that is 10–50x
slower — always use release mode when timing anything.

## Releasing

Tests run automatically on GitHub (`.github/workflows/ci.yml`); publishing to
PyPI is done manually. Thanks to abi3, each wheel covers Python 3.10+ on its
platform, and cross-compiling doesn't need a target Python interpreter.

`make wheels` builds the full release set (macOS wheel, both Linux wheels via
zig, sdist) and `make pypi` runs the tests, builds, and uploads. The
underlying commands:

```sh
# wheel for this machine + source distribution (lands in target/wheels/)
uvx maturin build --release
uvx maturin sdist

# optional: manylinux wheels cross-compiled from macOS via zig
rustup target add x86_64-unknown-linux-gnu aarch64-unknown-linux-gnu
uvx --with ziglang maturin build --release --zig --target x86_64-unknown-linux-gnu
uvx --with ziglang maturin build --release --zig --target aarch64-unknown-linux-gnu

# upload everything (needs a PyPI API token, e.g. via UV_PUBLISH_TOKEN)
uv publish target/wheels/*
```

Bump the version in `pyproject.toml` before building. Platforms without an
uploaded wheel (e.g. Windows) fall back to the sdist, which requires a Rust
toolchain to install.

## License

This project is MIT licensed. It statically links
[malachite](https://crates.io/crates/malachite) (LGPL-3.0-only) for
big-integer arithmetic; malachite's source is available on crates.io. If you
embed this library in a closed-source distribution, the LGPL relinking
requirements apply to the bundled malachite code.
