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

def condition_number(cov):
    eig_values = np.linalg.eigvalsh(cov)
    return eig_values.max() / eig_values.min()

def cov_stress_test(cov):
    """
    Stress a covariance matrix by progressively increasing
    the covariance between assets 1 and 2 toward perfect correlation.
    Returns eigenvalues, condition number, correlation and GMV weights.
    """
    # Define the assets that will be correlated
    var_a = cov[0, 0]
    var_b = cov[1, 1]
    perfect_cov = np.sqrt(var_a * var_b)

    # Create a new cov matrix as our target
    cov_target = cov.copy()
    cov_target[0, 1] = perfect_cov
    cov_target[1, 0] = perfect_cov

    # Create an array with the number of steps
    steps = np.array([0, 0.30, 0.650, 0.90, 0.99, 0.999])

    # Create the list where we will store the info of the test
    data_rows = []

    for alpha in steps:
        cov_step = (1 - alpha) * cov + alpha * cov_target
        eig_values = np.linalg.eigvalsh(cov_step)
        min_ev = eig_values.min()
        max_ev = eig_values.max()
        rho = cov_step[0, 1] / np.sqrt(cov_step[0, 0] * cov_step[1, 1])
        condition_number = max_ev / min_ev
        
        # GMV weights are not meaningful for a cov matrix that has eigenvalues < 0
        if min_ev > 1e-10:
            w1, w2, w3 = global_minimum_variance(cov_step)
        else:
            w1 = w2 = w3 = np.nan

        # Store the values of the test
        rows_dict = {
            "rho": rho,
            "min eigenvalue": min_ev,
            "max eigenvalue": max_ev,
            "condition number": condition_number,
            "w1": w1,
            "w2": w2,
            "w3": w3
        }

        data_rows.append(rows_dict)

    return pd.DataFrame(data_rows)