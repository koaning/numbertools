# Development

numbertoolkit is a [PyO3](https://pyo3.rs) extension module built with
[maturin](https://www.maturin.rs). The Rust sources live in `src/`, the
Python package wrapper in `python/numbertoolkit/`.

## Setup

Requires [Rust](https://rustup.rs) and [uv](https://docs.astral.sh/uv/).

```sh
make install                   # uv sync: build the extension and set up .venv
make test                      # cargo test + pytest
make bench                     # run the benchmark suite
make docs                      # live-reloading docs preview at localhost:8000
uvx maturin develop --uv -r    # fast rebuild loop (release mode)
```

Note: `maturin develop` without `-r` produces a debug build that is 10–50x
slower — always use release mode when timing anything.

## License

This project is MIT licensed. It statically links
[malachite](https://crates.io/crates/malachite) (LGPL-3.0-only) for
big-integer arithmetic; malachite's source is available on crates.io. If you
embed this library in a closed-source distribution, the LGPL relinking
requirements apply to the bundled malachite code.
