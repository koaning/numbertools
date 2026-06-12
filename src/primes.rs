//! Prime number utilities.

/// Return whether `n` is a prime number.
///
/// Anything below 2 (including negatives, 0 and 1) is not prime.
pub fn is_prime(n: i64) -> bool {
    if n < 2 {
        return false;
    }
    if n % 2 == 0 {
        return n == 2;
    }
    let mut d: i64 = 3;
    while (d as i128) * (d as i128) <= n as i128 {
        if n % d == 0 {
            return false;
        }
        d += 2;
    }
    true
}

/// Return the first `n` prime numbers in ascending order.
pub fn first_n_primes(n: usize) -> Vec<i64> {
    let mut primes = Vec::with_capacity(n);
    let mut candidate: i64 = 2;
    while primes.len() < n {
        if is_prime(candidate) {
            primes.push(candidate);
        }
        candidate += 1;
    }
    primes
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn small_primes() {
        assert!(is_prime(2));
        assert!(is_prime(3));
        assert!(is_prime(17));
        assert!(!is_prime(1));
        assert!(!is_prime(0));
        assert!(!is_prime(4));
        assert!(!is_prime(-7));
    }

    #[test]
    fn larger_prime() {
        assert!(is_prime(7919));
        assert!(!is_prime(7917));
    }

    #[test]
    fn first_few_primes() {
        assert_eq!(first_n_primes(5), vec![2, 3, 5, 7, 11]);
        assert_eq!(first_n_primes(1), vec![2]);
        assert_eq!(first_n_primes(0), Vec::<i64>::new());
    }

    #[test]
    fn generated_are_prime() {
        for p in first_n_primes(100) {
            assert!(is_prime(p));
        }
    }
}
