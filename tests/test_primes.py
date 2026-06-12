import pytest

from numbertoolkit import first_n_primes, is_prime


@pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 17, 7919])
def test_is_prime_true(n):
    assert is_prime(n) is True


@pytest.mark.parametrize("n", [-7, -1, 0, 1, 4, 9, 15, 100, 7917])
def test_is_prime_false(n):
    assert is_prime(n) is False


@pytest.mark.parametrize("bad", ["7", 3.5, None])
def test_is_prime_rejects_non_int(bad):
    with pytest.raises(TypeError):
        is_prime(bad)


def test_first_n_primes_values():
    assert first_n_primes(5) == [2, 3, 5, 7, 11]
    assert first_n_primes(1) == [2]
    assert first_n_primes(0) == []


@pytest.mark.parametrize("n", [10, 100, 1000])
def test_first_n_primes_length(n):
    assert len(first_n_primes(n)) == n


def test_first_n_primes_are_prime_and_sorted():
    primes = first_n_primes(200)
    assert all(is_prime(p) for p in primes)
    assert primes == sorted(primes)
    assert len(set(primes)) == len(primes)


def test_first_n_primes_rejects_negative():
    with pytest.raises(ValueError):
        first_n_primes(-1)


@pytest.mark.parametrize("bad", ["10", 3.5, None])
def test_first_n_primes_rejects_non_int(bad):
    with pytest.raises(TypeError):
        first_n_primes(bad)
