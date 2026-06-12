SHELL := /bin/bash

LINUX_TARGETS = x86_64-unknown-linux-gnu aarch64-unknown-linux-gnu

# Pyodide/wasm build: versions are pinned by pyodide-build for the current ABI
WASM_PY = 3.14
WASM_DIR = .wasm-toolchain
PYODIDE = uvx --from pyodide-build pyodide

.PHONY: install test bench docs wheels wasm-toolchain wasm-wheel pypi clean

# create .venv, build the extension, and install it editable with dev deps
install:
	uv sync

# uv run puts .venv/bin on PATH so pyo3's build script finds a working python3
test:
	uv run cargo test
	uv run pytest

bench:
	uv run --group bench benchmarks/bench_pi.py
	uv run --group bench benchmarks/bench_e.py
	uv run --group bench benchmarks/bench_sqrt.py

# live-reloading docs preview at http://localhost:8000
docs:
	uv run zensical serve

# build the full release set: macOS wheel, Linux wheels (via zig), sdist
wheels:
	rm -rf target/wheels
	rustup target add $(LINUX_TARGETS)
	uvx maturin build --release
	$(foreach target,$(LINUX_TARGETS),uvx --with ziglang maturin build --release --zig --target $(target) &&) true
	uvx maturin sdist
	@ls -lh target/wheels

# one-time setup for the Pyodide wheel: emsdk + the rust toolchain the current
# Pyodide ABI is built against (macOS is unsupported-but-works for this; the
# officially supported host is Linux)
wasm-toolchain:
	test -d $(WASM_DIR)/emsdk || git clone https://github.com/emscripten-core/emsdk $(WASM_DIR)/emsdk
	uv python install $(WASM_PY)
	EMSDK_VER=$$($(PYODIDE) config get emscripten_version) && \
	  export EMSDK_PYTHON=$$(uv python find $(WASM_PY)) && \
	  cd $(WASM_DIR)/emsdk && ./emsdk install $$EMSDK_VER && ./emsdk activate $$EMSDK_VER
	RUST_VER=$$($(PYODIDE) config get rust_toolchain) && \
	  rustup toolchain install $$RUST_VER && \
	  rustup target add wasm32-unknown-emscripten --toolchain $$RUST_VER

# Pyodide wheel (PEP 783 pyemscripten tag) so micropip can install from PyPI.
# MATURIN_PYEMSCRIPTEN_PLATFORM_VERSION forces the PEP 783 tag — without it
# maturin may fall back to a legacy pyodide_* tag that PyPI rejects, hence the
# trailing ls assertion.
wasm-wheel: wasm-toolchain
	export EMSDK_PYTHON=$$(uv python find $(WASM_PY)) && \
	  source $(WASM_DIR)/emsdk/emsdk_env.sh && \
	  RUSTUP_TOOLCHAIN=$$($(PYODIDE) config get rust_toolchain) \
	  MATURIN_PYEMSCRIPTEN_PLATFORM_VERSION=$$($(PYODIDE) config get pyodide_abi_version) \
	  CARGO_TARGET_WASM32_UNKNOWN_EMSCRIPTEN_RUSTFLAGS="$$($(PYODIDE) config get rustflags)" \
	  uvx maturin build --release --target wasm32-unknown-emscripten -i $$(uv python find $(WASM_PY))
	@ls target/wheels/*pyemscripten_*_wasm32.whl

pypi: test wheels wasm-wheel
	uv publish target/wheels/*

clean:
	cargo clean
	rm -rf .venv .pytest_cache site .zensical
