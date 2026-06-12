mod pi;
mod primes;

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

/// Return the first `n` significant digits of pi as a string.
///
/// Digits are truncated, not rounded: `pi_digits(5) == "3.1415"`.
#[pyfunction]
fn pi_digits(py: Python<'_>, n: i64) -> PyResult<String> {
    if n < 1 {
        return Err(PyValueError::new_err("n must be >= 1"));
    }
    Ok(py.detach(|| pi::pi_digits(n as usize)))
}

/// Return whether `n` is a prime number.
///
/// Anything below 2 (including negatives, 0 and 1) is not prime.
#[pyfunction]
fn is_prime(n: i64) -> PyResult<bool> {
    Ok(primes::is_prime(n))
}

/// Return the first `n` prime numbers in ascending order.
#[pyfunction]
fn first_n_primes(n: i64) -> PyResult<Vec<i64>> {
    if n < 0 {
        return Err(PyValueError::new_err("n must be >= 0"));
    }
    Ok(primes::first_n_primes(n as usize))
}

#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(pi_digits, m)?)?;
    m.add_function(wrap_pyfunction!(is_prime, m)?)?;
    m.add_function(wrap_pyfunction!(first_n_primes, m)?)?;
    Ok(())
}
