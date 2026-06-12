mod e;
mod phi;
mod pi;
mod primes;
mod sqrt;

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

/// Return the first `n` significant digits of pi as a raw digit string.
///
/// Digits are truncated, not rounded: `pi_digits(5) == "31415"`.
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

/// Return the first `n` significant digits of e as a raw digit string.
///
/// Digits are truncated, not rounded: `e_digits(5) == "27182"`.
#[pyfunction]
fn e_digits(py: Python<'_>, n: i64) -> PyResult<String> {
    if n < 1 {
        return Err(PyValueError::new_err("n must be >= 1"));
    }
    Ok(py.detach(|| e::e_digits(n as usize)))
}

/// Return the first `n` significant digits of the golden ratio as a raw
/// digit string.
///
/// Digits are truncated, not rounded: `phi_digits(5) == "16180"`.
#[pyfunction]
fn phi_digits(py: Python<'_>, n: i64) -> PyResult<String> {
    if n < 1 {
        return Err(PyValueError::new_err("n must be >= 1"));
    }
    Ok(py.detach(|| phi::phi_digits(n as usize)))
}

/// Return the first `n` significant digits of sqrt(d) as a string.
///
/// Digits are truncated, not rounded: `sqrt_digits(2, 5) == "1.4142"`.
#[pyfunction]
fn sqrt_digits(py: Python<'_>, d: i64, n: i64) -> PyResult<String> {
    if d < 1 {
        return Err(PyValueError::new_err("d must be >= 1"));
    }
    if n < 1 {
        return Err(PyValueError::new_err("n must be >= 1"));
    }
    Ok(py.detach(|| sqrt::sqrt_digits(d as u64, n as usize)))
}

#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(pi_digits, m)?)?;
    m.add_function(wrap_pyfunction!(is_prime, m)?)?;
    m.add_function(wrap_pyfunction!(first_n_primes, m)?)?;
    m.add_function(wrap_pyfunction!(e_digits, m)?)?;
    m.add_function(wrap_pyfunction!(phi_digits, m)?)?;
    m.add_function(wrap_pyfunction!(sqrt_digits, m)?)?;
    Ok(())
}
