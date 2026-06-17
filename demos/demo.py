import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # numbertoolkit demo

    `numbertoolkit` is a Python library for playing with number theory topics, with
    the heavy lifting done in Rust. It computes the digits of famous constants —
    `pi_digits(n)`, `e_digits(n)`, and `phi_digits(n)` — as raw digit streams,
    using binary splitting and exact integer arithmetic all the way down, no
    floating point. Pass `decimal_point=True` if you want the point back.
    """)
    return


@app.cell
def _():
    import time

    import marimo as mo

    import numbertoolkit

    return mo, numbertoolkit, time


@app.cell
def _(mo, numbertoolkit):
    constant = mo.ui.dropdown(
        {
            "pi": numbertoolkit.pi_digits,
            "e": numbertoolkit.e_digits,
            "phi": numbertoolkit.phi_digits,
        },
        value="pi",
        label="Constant",
    )
    n = mo.ui.slider(
        1, 10_000, value=50, label="Number of digits", show_value=True, full_width=True
    )
    mo.vstack([constant, n])
    return constant, n


@app.cell
def _(constant, mo, n):
    digits = constant.value(n.value)
    wrapped = "\n".join(digits[i : i + 80] for i in range(0, len(digits), 80))
    mo.md(
        f"**The first {n.value:,} digits of {constant.selected_key}**\n\n```\n{wrapped}\n```"
    )
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
def _(constant, mo, time):
    rows = []
    for size in (1_000, 10_000, 100_000, 1_000_000):
        start = time.perf_counter()
        constant.value(size)
        rows.append((size, time.perf_counter() - start))
    mo.md(
        f"Timings for **{constant.selected_key}**:\n\n"
        + "| digits | seconds |\n|---:|---:|\n"
        + "\n".join(f"| {size:,} | {secs:.3f} |" for size, secs in rows)
    )
    return


if __name__ == "__main__":
    app.run()
