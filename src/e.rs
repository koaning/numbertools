//! Factorial series for e with binary splitting.
//!
//! e = sum_{k=0}^{inf} 1/k!
//!
//! For a range [a, b), `bsplit` returns (P, Q) with
//! P/Q = sum_{k=a}^{b-1} 1/(a (a+1) ... k), so P(1, N+1)/Q(1, N+1) =
//! sum_{k=1}^{N} 1/k! and e = 1 + P/Q. All arithmetic is exact natural-number
//! arithmetic scaled by 10^prec, so the output is floor(e * 10^prec)
//! truncated to n significant digits.

use malachite::base::num::arithmetic::traits::Pow;
use malachite::Natural;

const GUARD: usize = 12;

/// Binary splitting over factorial-series terms k in [a, b).
///
/// Returns (P, Q) such that P/Q = sum_{k=a}^{b-1} 1/(a (a+1) ... k)
/// (with Q the running product a (a+1) ... (b-1) needed to merge ranges).
fn bsplit(a: u64, b: u64) -> (Natural, Natural) {
    if b - a == 1 {
        (Natural::from(1u32), Natural::from(a))
    } else {
        let m = a + (b - a) / 2;
        let (p1, q1) = bsplit(a, m);
        let (p2, q2) = bsplit(m, b);
        (&p1 * &q2 + p2, q1 * q2)
    }
}

/// Smallest N (with one digit of slack) such that the series tail after N
/// terms is below 10^-(prec+1), i.e. log10(N!) > prec + 1.
fn terms_for(prec: usize) -> u64 {
    let target = prec as f64 + 1.0;
    let mut log10_factorial = 0.0;
    let mut k = 0u64;
    while log10_factorial <= target {
        k += 1;
        log10_factorial += (k as f64).log10();
    }
    k
}

/// First `n` significant digits of e as a raw digit string, truncated:
/// `e_digits(5) == "27182"`.
pub fn e_digits(n: usize) -> String {
    let prec = n + GUARD;
    let (p, q) = bsplit(1, terms_for(prec) + 1);
    // e = 1 + P/Q; the k = 0 term is folded in as Q + P.
    let s = (Natural::from(10u32).pow(prec as u64) * (&q + &p) / q).to_string();
    s[..n].to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn small_values() {
        assert_eq!(e_digits(1), "2");
        assert_eq!(e_digits(2), "27");
        assert_eq!(e_digits(5), "27182");
        assert_eq!(e_digits(10), "2718281828");
    }

    #[test]
    fn fifty_decimals() {
        assert_eq!(
            e_digits(51),
            "271828182845904523536028747135266249775724709369995"
        );
    }

    #[test]
    fn bsplit_base_case() {
        // [a, a+1): P/Q = 1/a
        let (p, q) = bsplit(7, 8);
        assert_eq!(p, Natural::from(1u32));
        assert_eq!(q, Natural::from(7u32));
        // [1, 4): P/Q = 1/1! + 1/2! + 1/3! = 10/6
        let (p, q) = bsplit(1, 4);
        assert_eq!(p, Natural::from(10u32));
        assert_eq!(q, Natural::from(6u32));
    }

    #[test]
    fn terms_for_sanity() {
        // log10(70!) ~ 100.08, so ~71 terms suffice for 100 digits
        let n = terms_for(100);
        assert!((70..=75).contains(&n), "terms_for(100) = {n}");
    }
}
