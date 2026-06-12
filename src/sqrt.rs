//! Digits of sqrt(d) via exact integer floor_sqrt.
//!
//! floor_sqrt(d * 10^(2*prec)) == floor(sqrt(d) * 10^prec) exactly, so the
//! output is floor(sqrt(d) * 10^prec) truncated to n significant digits.
//! No floating point and no division are involved.

use malachite::base::num::arithmetic::traits::{FloorSqrt, Pow};
use malachite::Natural;

/// First `n` significant digits of sqrt(d), truncated:
/// `sqrt_digits(2, 5) == "1.4142"`, `sqrt_digits(3, 5) == "1.7320"`.
///
/// No guard digits: floor_sqrt is exact and floor(floor(x)/m) == floor(x/m),
/// so prec = n already yields the exact truncated prefix.
pub fn sqrt_digits(d: u64, n: usize) -> String {
    let prec = n;
    let radicand = Natural::from(d) * Natural::from(10u32).pow(2 * prec as u64);
    let s = radicand.floor_sqrt().to_string(); // digits of sqrt(d), no point
    // Integer part occupies the leading (len - prec) characters.
    let int_len = s.len() - prec;
    if n <= int_len {
        s[..n].to_string()
    } else {
        format!("{}.{}", &s[..int_len], &s[int_len..n])
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn small_values() {
        assert_eq!(sqrt_digits(2, 1), "1");
        assert_eq!(sqrt_digits(2, 5), "1.4142");
        assert_eq!(sqrt_digits(3, 5), "1.7320");
        assert_eq!(sqrt_digits(2, 10), "1.414213562");
    }

    #[test]
    fn fifty_decimals() {
        assert_eq!(
            sqrt_digits(2, 51),
            "1.41421356237309504880168872420969807856967187537694"
        );
        assert_eq!(
            sqrt_digits(3, 51),
            "1.73205080756887729352744634150587236694280525381038"
        );
    }

    #[test]
    fn perfect_square_has_trailing_zeros() {
        assert_eq!(sqrt_digits(4, 5), "2.0000");
        assert_eq!(sqrt_digits(9, 3), "3.00");
    }

    #[test]
    fn multi_digit_integer_part() {
        // sqrt(200) = 14.14213562...
        assert_eq!(sqrt_digits(200, 4), "14.14");
        assert_eq!(sqrt_digits(200, 2), "14");
    }
}
