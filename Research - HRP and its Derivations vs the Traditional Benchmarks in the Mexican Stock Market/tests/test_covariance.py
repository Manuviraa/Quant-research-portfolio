import numpy as np
import pytest

from src.covariance import (sample_covariance,  
                            gmv_setup)

from src.portfolio_math import portfolio_variance

# The sample covariance function matches the output of np.cov()
def test_sample_cov_matches_numpy_cov():
    rng = np.random.default_rng(42)
    R = rng.standard_normal((100, 5))
    S = sample_covariance(R)
    assert np.allclose(S, np.cov(R, rowvar=False))

# Sample covariance of the returns is symmetric and positive semi-definite
def test_S_is_symmetric_and_PSD():
    rng = np.random.default_rng(42)
    R = rng.standard_normal((10, 20))
    
    S = sample_covariance(R)
    eigs = np.linalg.eigvalsh(S)
    eig_min, eig_max = eigs[0], eigs[-1]
    tol = eig_max * S.shape[0] * np.finfo(float).eps
    
    assert np.allclose(S, S.T)
    assert eig_min >= -tol

# Rank of the sample covariance matrix is <= T-1
def test_sample_cov_rank_leq_t_minus_1():
    T, N = 10, 20
    rng = np.random.default_rng(42)
    R = rng.standard_normal((T,N))
    S = sample_covariance(R)
    rank_S = np.linalg.matrix_rank(S)
    assert rank_S <= (T - 1)

# Reported GMV <= w* under S
@pytest.mark.parametrize("seed", range(20))
@pytest.mark.parametrize("T", [40, 100, 1000])
def test_reported_gmv_variance_leq_w_star_under_S(seed, T):
    Sigma, S, w_star, w_hat = gmv_setup(seed, T)
    left = portfolio_variance(w_hat, S)
    right = portfolio_variance(w_star, S)
    assert left <= right * (1 + 1e-10)

# True GMV <= ŵ under Σ)
@pytest.mark.parametrize("seed", range(20))
@pytest.mark.parametrize("T", [40, 100, 1000])
def test_true_gmv_variance_leq_w_hat_under_Sigma(seed, T):
    Sigma, S, w_star, w_hat = gmv_setup(seed, T)
    left = portfolio_variance(w_star, Sigma)
    right = portfolio_variance(w_hat, Sigma)
    assert left <= right * (1 + 1e-10)