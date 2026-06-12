//! The golden ratio phi = (1 + sqrt(5)) / 2.
//!
//! floor(phi * 10^prec) = (10^prec + floor_sqrt(5 * 10^(2 prec))) / 2 holds
//! exactly: sqrt(5) * 10^prec is irrational, so taking the floor of the
//! square root before halving never changes the overall floor. The output is
//! therefore the exact digits of phi truncated to n significant digits.

use malachite::base::num::arithmetic::traits::{FloorSqrt, Pow};
use malachite::Natural;

const GUARD: usize = 12;

/// First `n` significant digits of phi as a raw digit string, truncated:
/// `phi_digits(5) == "16180"`.
pub fn phi_digits(n: usize) -> String {
    let prec = (n + GUARD) as u64;
    let sqrt5 = (Natural::from(5u32) * Natural::from(10u32).pow(2 * prec)).floor_sqrt();
    let s = ((Natural::from(10u32).pow(prec) + sqrt5) / Natural::from(2u32)).to_string();
    s[..n].to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn small_values() {
        assert_eq!(phi_digits(1), "1");
        assert_eq!(phi_digits(2), "16");
        assert_eq!(phi_digits(5), "16180");
        assert_eq!(phi_digits(10), "1618033988");
    }

    #[test]
    fn fifty_decimals() {
        assert_eq!(
            phi_digits(51),
            "161803398874989484820458683436563811772030917980576"
        );
    }
}
