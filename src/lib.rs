mod pi;
mod sqrt;

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
    m.add_function(wrap_pyfunction!(sqrt_digits, m)?)?;
    Ok(())
}
