import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Are the digits random?

    The digits of `pi`, `e`, and `sqrt(2)` are all *conjectured* to be **normal**:
    every digit, every pair, every triple should show up equally often in the long
    run. Nobody has ever proven it, so the only thing we can do is look.

    This notebook does the simplest possible thing. It counts how often each digit
    `0`–`9` appears, then each pair `00`–`99`, then each triple `000`–`999`, and
    asks whether those counts are consistent with truly random digits. As a control
    it runs the exact same checks against a real pseudo-random number generator.

    The model is a binomial one: if digits were random, each of the `10**k` possible
    `k`-grams turns up with probability `10**-k`, so its count over `m` groups is
    `Binomial(m, 10**-k)`. For each category we compute a two-sided p-value (normal
    approximation to the binomial, stdlib only) and call it a **fail** when the
    p-value drops below the significance level you pick.
    """)
    return


@app.cell
def _():
    import itertools
    import math
    import random
    from collections import Counter

    import marimo as mo

    import numbertoolkit

    return Counter, itertools, math, mo, numbertoolkit, random


@app.cell
def _(Counter, itertools, math):
    LEVELS = {1: "single digits", 2: "pairs", 3: "triples"}

    def category_stats(digits, k, alpha):
        """Test every one of the 10**k possible non-overlapping k-grams against
        Binomial(m, 10**-k). Returns (rows, passed, failed, m), where each row is
        (gram, count, expected, z, p_value, passed?)."""
        m = len(digits) // k
        p = 10**-k
        expected = m * p
        sd = math.sqrt(m * p * (1 - p))
        if k == 1:
            counts = Counter(digits)
        else:
            # group into non-overlapping k-tuples (drops any trailing remainder)
            counts = Counter(map("".join, zip(*[iter(digits)] * k)))
        rows = []
        passed = 0
        for combo in itertools.product("0123456789", repeat=k):
            gram = "".join(combo)
            count = counts.get(gram, 0)
            z = 0.0 if sd == 0 else (count - expected) / sd
            pval = 1.0 if sd == 0 else math.erfc(abs(z) / math.sqrt(2))
            ok = pval >= alpha
            passed += ok
            rows.append((gram, count, expected, z, pval, ok))
        return rows, passed, len(rows) - passed, m

    def kgram_fail_count(digits, k, alpha):
        """Just the failure tally for the summary table."""
        _, _, failed, m = category_stats(digits, k, alpha)
        return failed, 10**k, m

    return LEVELS, category_stats, kgram_fail_count


@app.cell
def _(mo, numbertoolkit):
    source = mo.ui.dropdown(
        {
            "pi": lambda n: numbertoolkit.pi_digits(n),
            "e": lambda n: numbertoolkit.e_digits(n),
            "sqrt(2)": lambda n: numbertoolkit.sqrt_digits(2, n, decimal_point=False),
        },
        value="pi",
        label="Constant",
    )
    n = mo.ui.slider(
        1_000,
        10_000_000,
        value=100_000,
        step=1_000,
        label="Number of digits",
        show_value=True,
        full_width=True,
    )
    alpha = mo.ui.slider(
        0.1,
        10.0,
        value=5.0,
        step=0.1,
        label="Significance level (%)",
        show_value=True,
        full_width=True,
    )
    seed = mo.ui.number(0, 9999, value=0, label="PRNG seed")
    mo.vstack([source, mo.hstack([n, alpha], widths="equal", gap=2), seed])
    return alpha, n, seed, source


@app.cell
def _(n, random, seed):
    rng = random.Random(seed.value)
    prng_digits = "".join(rng.choices("0123456789", k=n.value))
    return (prng_digits,)


@app.cell
def _(n, source):
    const_digits = source.value(n.value)
    return (const_digits,)


@app.cell
def _(alpha, const_digits, kgram_fail_count, mo, n, prng_digits, source):
    a = alpha.value / 100

    def row(label, digits):
        cells = []
        for k in (1, 2, 3):
            failures, total, _ = kgram_fail_count(digits, k, a)
            cells.append(f"{failures} / {total}")
        return f"| {label} | " + " | ".join(cells) + " |"

    expected = " | ".join(f"~{a * 10**k:.0f} / {10**k}" for k in (1, 2, 3))
    mo.md(
        f"## Categories that fail the randomness check\n\n"
        f"Across **{n.value:,} digits** at a **{alpha.value:g}%** significance "
        f"level. Each cell is `failed / total` categories.\n\n"
        f"| source | digits (0–9) | pairs (00–99) | triples (000–999) |\n"
        f"|---|---:|---:|---:|\n"
        f"{row(source.selected_key, const_digits)}\n"
        f"{row('PRNG (control)', prng_digits)}\n"
        f"| **expected by chance** | {expected} |\n\n"
        f"By pure chance roughly **{alpha.value:g}%** of categories fail even for "
        f"truly random digits — that's what the *expected* row shows. The constant "
        f"is suspicious only if it fails *far* more than that. Spoiler: `pi`, `e`, "
        f"and `sqrt(2)` are conjectured normal, so they should sit right alongside "
        f"the PRNG."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## A closer look, by category

    The summary above only counts pass/fail. To actually *see* the categories you
    can break it down per group — but a full listing explodes fast: 10 single
    digits, 100 pairs, **1000** triples. So for pairs and triples we don't dump
    every row; we show the handful that deviate most from what randomness predicts
    (largest `|z|`). Single digits are few enough to list in full.
    """)
    return


@app.cell
def _(mo):
    detail_k = mo.ui.dropdown(
        {"single digits (0–9)": 1, "pairs (00–99)": 2, "triples (000–999)": 3},
        value="single digits (0–9)",
        label="Detail level",
    )
    detail_k
    return (detail_k,)


@app.cell
def _(LEVELS, alpha, category_stats, const_digits, detail_k, mo, source):
    DETAIL_TOP = 20
    a3 = alpha.value / 100
    k = detail_k.value
    rows, passed, failed, m = category_stats(const_digits, k, a3)
    total = 10**k

    if k == 1:
        shown = sorted(rows, key=lambda r: r[0])  # natural 0–9 order
        caption = f"All {total} {LEVELS[k]} in **{source.selected_key}**:"
    else:
        shown = sorted(rows, key=lambda r: -abs(r[3]))[:DETAIL_TOP]
        caption = (
            f"The {len(shown)} most extreme of {total:,} {LEVELS[k]} in "
            f"**{source.selected_key}** (by deviation). Overall **{passed:,} "
            f"passed / {failed:,} failed** — expected ~{a3 * total:.0f} failures "
            f"by chance."
        )

    body = "\n".join(
        f"| `{gram}` | {count:,} | {exp:,.1f} | {z:+.2f} | {pval:.3f} | "
        f"{'✓' if ok else '✗'} |"
        for gram, count, exp, z, pval, ok in shown
    )
    mo.md(
        f"{caption}\n\n"
        f"| group | count | expected | z | p-value | pass |\n"
        f"|:--|---:|---:|---:|---:|:--:|\n"
        f"{body}"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### A note on reading this

    Three things to keep in mind:

    - **Failing is normal.** At a 5% significance level, about 5% of categories are
      *supposed* to fail on random data. A handful of failures means nothing — only
      a wildly higher failure rate would be evidence against randomness.
    - **The normal approximation needs volume.** Each category is expected only
      `m / 10**k` times, so the binomial-to-normal approximation is only trustworthy
      when that expected count isn't tiny. For triples the 100,000-digit default
      puts it around 33, which is comfortable; cranking the digit count way down (or
      `k` up) makes the triples view shaky — push the slider toward 10 million for a
      cleaner read.
    - **10 million digits is heavy.** The digits compute in a flash, but counting
      them in pure Python (twice, for the constant and the control) takes a few
      seconds. That's the price of no numpy.
    """)
    return


if __name__ == "__main__":
    app.run()
