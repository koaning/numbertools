mod e;
mod phi;
mod pi;

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

#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(pi_digits, m)?)?;
    m.add_function(wrap_pyfunction!(e_digits, m)?)?;
    m.add_function(wrap_pyfunction!(phi_digits, m)?)?;
    Ok(())
}
