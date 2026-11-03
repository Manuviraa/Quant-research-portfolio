import numpy as np

from src.covariance import sample_covariance

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