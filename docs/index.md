# numbertoolkit

Fast number theory utilities for Python, backed by Rust.

```python
import numbertoolkit

numbertoolkit.pi_digits(10)
# '3.141592653'
```

<iframe src="https://marimo.app/github/koaning/numbertools/blob/main/demo.py?embed=true" sandbox="allow-scripts allow-same-origin allow-downloads allow-popups allow-forms" allow="microphone" allowfullscreen width="100%" height="700" frameborder="0"></iframe>

The heavy lifting happens in a compiled Rust extension using exact integer
arithmetic, so results are correct to the last digit and stay fast well into
the millions of digits.

## Installation

```sh
pip install numbertoolkit
```

Wheels are published for Python 3.10+ on macOS and Linux. On platforms
without a wheel, pip falls back to the source distribution, which requires a
[Rust toolchain](https://rustup.rs) to build.

## Quickstart

```python
from numbertoolkit import pi_digits

pi_digits(5)
# '3.1415'

len(pi_digits(1_000_000))  # a million digits in a fraction of a second
# 1000001
```

Digits are truncated, not rounded — see the [API reference](api.md) for
details.

## Learn more

- [API reference](api.md) — full documentation of `pi_digits`
- [Benchmarks](benchmarks.md) — how it compares to mpmath
- [Development](development.md) — building, testing, and releasing
