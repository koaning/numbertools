LINUX_TARGETS = x86_64-unknown-linux-gnu aarch64-unknown-linux-gnu

.PHONY: install test bench wheels pypi clean

# create .venv, build the extension, and install it editable with dev deps
install:
	uv sync

# uv run puts .venv/bin on PATH so pyo3's build script finds a working python3
test:
	uv run cargo test
	uv run pytest

bench:
	uv run --group bench benchmarks/bench_pi.py

# build the full release set: macOS wheel, Linux wheels (via zig), sdist
wheels:
	rm -rf target/wheels
	rustup target add $(LINUX_TARGETS)
	uvx maturin build --release
	$(foreach target,$(LINUX_TARGETS),uvx --with ziglang maturin build --release --zig --target $(target) &&) true
	uvx maturin sdist
	@ls -lh target/wheels

pypi: test wheels
	uv publish target/wheels/*

clean:
	cargo clean
	rm -rf .venv .pytest_cache
