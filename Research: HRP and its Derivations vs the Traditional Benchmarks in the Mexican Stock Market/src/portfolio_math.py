import numpy as np
import pandas as pd

def portfolio_return(weights, mu):
    return weights @ mu

def portfolio_variance(weights, cov):
    if weights.ndim == 1:
        return weights.T @ cov @ weights
    else:
        return ((weights@ cov) * weights).sum(axis=1)

def portfolio_volatility(weights, cov):
    return np.sqrt(portfolio_variance(weights, cov))

def global_minimum_variance(cov):
    J = np.ones(cov.shape[0])
    inv_cov = np.linalg.inv(cov)
    return (inv_cov @ J) / (J.T @ inv_cov @ J)

def efficient_portfolio(mu, cov, target_return):
    #1. Create the vectors
    J = np.ones(cov.shape[0])
    A = np.column_stack((J, mu))
    b = np.array([1, target_return])

    # 2. Compute \Sigma{^-1} @ A
    cov_inv_A = np.linalg.solve(cov, A)

    #3. Compute the central block
    central_block = A.T @ cov_inv_A

    # 4. Compute gamma
    gamma = np.linalg.solve(central_block, b)

    #5. Compute the portfolio weights
    return cov_inv_A @ gamma

def efficient_frontier(mu, cov, n_points=100):

    # Given that the efficient frontier extends upwards from the Global Minimum Variance portfolio, we will take this as our starting point.
    gmv_weights = global_minimum_variance(cov)

    # Compute the minimum and maximum return from the assets
    start_point = gmv_weights @ mu
    end_point = np.max(mu)
    target_returns = np.linspace(start_point, end_point, n_points)

    # Save the results
    portfolio_risks = []
    portfolio_returns =[]
    portfolio_weights = []

    # Iterate on every portfolio
    for target in target_returns:
        w = efficient_portfolio(mu, cov, target)

        variance = w.T @ cov @ w
        risk = np.sqrt(variance)
        returns = w @ mu

        # Save the results
        portfolio_risks.append(risk)
        portfolio_returns.append(returns)
        portfolio_weights.append(w)

    # Finally, we return an array for each result list
    return np.array(portfolio_risks), np.array(portfolio_returns), np.array(portfolio_weights)
