//! Chudnovsky algorithm with binary splitting.
//!
//! pi = 426880 * sqrt(10005) / sum_{k=0}^{inf} (-1)^k (6k)! (13591409 + 545140134 k)
//!                                              / ((3k)! (k!)^3 640320^(3k))
//!
//! All arithmetic is exact integer arithmetic scaled by 10^prec; the square
//! root is an exact integer floor_sqrt. No floating point is involved, so the
//! output is floor(pi * 10^prec) truncated to n significant digits.

use malachite::base::num::arithmetic::traits::{FloorSqrt, Pow};
use malachite::{Integer, Natural};

const A: u64 = 13_591_409;
const B: u64 = 545_140_134;
const C3_OVER_24: u64 = 10_939_058_860_032_000; // 640320^3 / 24
const DIGITS_PER_TERM: f64 = 14.181647462725477;
const GUARD: usize = 12;

/// Binary splitting over Chudnovsky terms k in [a, b).
///
/// Returns (P, Q, T) such that the partial sum of terms a..b equals T / Q
/// (with P the running product needed to merge adjacent ranges).
fn bsplit(a: u64, b: u64) -> (Integer, Integer, Integer) {
    if b - a == 1 {
        let p = Integer::from(6 * a - 5) * Integer::from(2 * a - 1) * Integer::from(6 * a - 1);
        let q = Integer::from(a).pow(3) * Integer::from(C3_OVER_24);
        let mut t = &p * Integer::from(A + B * a);
        if a & 1 == 1 {
            t = -t;
        }
        (p, q, t)
    } else {
        let m = a + (b - a) / 2;
        let (p1, q1, t1) = bsplit(a, m);
        let (p2, q2, t2) = bsplit(m, b);
        (&p1 * &p2, &q1 * &q2, &t1 * &q2 + &p1 * &t2)
    }
}

/// First `n` significant digits of pi as a raw digit string, truncated:
/// `pi_digits(5) == "31415"`.
pub fn pi_digits(n: usize) -> String {
    let prec = n + GUARD;
    let terms = ((prec as f64 / DIGITS_PER_TERM) as u64 + 1).max(2);
    // The k = 0 term (P=Q=1, T=A) is folded in below as A*Q + T.
    let (_p, q, t) = bsplit(1, terms);
    let sqrt_c = (Natural::from(10_005u32) * Natural::from(10u32).pow(2 * prec as u64)).floor_sqrt();
    let numer = Integer::from(426_880u32) * Integer::from(sqrt_c) * &q;
    let denom = Integer::from(A) * &q + &t;
    let s = (numer / denom).to_string(); // "31415926..." = floor(pi * 10^prec)
    s[..n].to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn small_values() {
        assert_eq!(pi_digits(1), "3");
        assert_eq!(pi_digits(2), "31");
        assert_eq!(pi_digits(5), "31415");
        assert_eq!(pi_digits(10), "3141592653");
    }

    #[test]
    fn fifty_decimals() {
        assert_eq!(
            pi_digits(51),
            "314159265358979323846264338327950288419716939937510"
        );
    }

    #[test]
    fn bsplit_base_case() {
        // k = 1: p = 1*1*5 = 5, q = 640320^3/24, t = -5 * (A + B)
        let (p, q, t) = bsplit(1, 2);
        assert_eq!(p, Integer::from(5u32));
        assert_eq!(q, Integer::from(C3_OVER_24));
        assert_eq!(t, -Integer::from(5 * (A + B)));
    }
}
