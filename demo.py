import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # numbertoolkit demo

    `numbertoolkit` is a Python library for playing with number theory topics, with
    the heavy lifting done in Rust. Its first function is `pi_digits(n)`, which
    returns the first `n` significant digits of pi as a string, computed with the
    Chudnovsky series and binary splitting — exact integer arithmetic all the way
    down, no floating point.
    """)
    return


@app.cell
def _():
    import time

    import marimo as mo

    import numbertoolkit

    return mo, numbertoolkit, time


@app.cell
def _(mo):
    n = mo.ui.slider(
        1, 10_000, value=50, label="Number of digits", show_value=True, full_width=True
    )
    n
    return (n,)


@app.cell
def _(mo, n, numbertoolkit):
    digits = numbertoolkit.pi_digits(n.value)
    wrapped = "\n".join(digits[i : i + 80] for i in range(0, len(digits), 80))
    mo.md(f"**The first {n.value:,} digits of pi**\n\n```\n{wrapped}\n```")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## How fast is it?

    Binary splitting makes the cost quasi-linear in the number of digits, so even
    a million digits only takes a fraction of a second. Timed live in this
    notebook:
    """)
    return


@app.cell
def _(mo, numbertoolkit, time):
    rows = []
    for size in (1_000, 10_000, 100_000, 1_000_000):
        start = time.perf_counter()
        numbertoolkit.pi_digits(size)
        rows.append((size, time.perf_counter() - start))
    mo.md(
        "| digits | seconds |\n|---:|---:|\n"
        + "\n".join(f"| {size:,} | {secs:.3f} |" for size, secs in rows)
    )
    return


if __name__ == "__main__":
    app.run()
