mod pi;

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

#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(pi_digits, m)?)?;
    Ok(())
}
