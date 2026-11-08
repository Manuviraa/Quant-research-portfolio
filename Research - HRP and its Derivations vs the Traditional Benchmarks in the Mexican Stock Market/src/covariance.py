import numpy as np
from src.portfolio_math import global_minimum_variance

def sample_covariance(returns):
    #1. Number of assets
    T_obs = returns.shape[0]
    #2. Mean
    mu = returns.mean(axis=0, keepdims = True)
    # 3.Demeaned returns
    demeaned_returns = returns - mu
    #4. Sample covariance
    return (demeaned_returns.T @ demeaned_returns) / (T_obs - 1)

def spectrum_stats(S):
    """
    Inputs a covariance matrix
    Returns the spectrum stats in the following order:
    Ordered eigenvalues, Min eigenvalue, Max eigenvalue, Condition number
    """
    eigs = np.linalg.eigvalsh(S)
    eig_min, eig_max = eigs[0], eigs[-1]
    tol = eig_max * S.shape[0] * np.finfo(float).eps
    condition_number = np.inf if eig_min <= tol else eig_max / eig_min
    
    return eigs, eig_min, eig_max, condition_number

def relative_frobenius_error(Sigma, S):
    """
    Inputs a true covariance matrix and an estimation
    Outputs the Relative Frobenius Error
    """
    return np.linalg.norm(S - Sigma, 'fro') / np.linalg.norm(Sigma, 'fro')

def simulate_returns(Sigma, T, rng, mu=None):
    L = np.linalg.cholesky(Sigma) # 1. Apply Cholesky decomposition to the covariance matrix Sigma
    N = Sigma.shape[0]
    Z = rng.standard_normal((T, N)) # 2. Generate random noise. Mean 0, standard deviation 1
    R = Z @ L.T # 3. Compute the returns

    if mu is not None:
        R = R + mu

    return R

def one_factor_covariance(N, seed, sigma_m=0.01,
                          beta_range=(0.5, 1.5), idio_range=(0.01, 0.02)):
    
    """
    Inputs the number of assets, a random seed, market volatility, and ranges for beta and idiosyncratic volatility.
    Outputs a true multi-asset covariance matrix based on a single-factor model structure.
    """
    rng = np.random.default_rng(seed)

    beta = rng.uniform(*beta_range, size=N)
    idio_vol = rng.uniform(*idio_range, size=N)

    Sigma = sigma_m**2 * np.outer(beta, beta) + np.diag(idio_vol**2)
    
    return Sigma

def gmv_setup(seed, T, N=35):
    """
    Inputs a random seed, the number of time periods T, and the number of assets N.
    Outputs a tuple containing the true covariance (Sigma), the sample covariance (S), 
    and the Global Minimum Variance weights for both matrices.
    """
    Sigma = one_factor_covariance(N, seed=42)
    rng = np.random.default_rng(seed)
    R = simulate_returns(Sigma, T, rng)
    S = sample_covariance(R)
    return Sigma, S, global_minimum_variance(Sigma), global_minimum_variance(S)
    