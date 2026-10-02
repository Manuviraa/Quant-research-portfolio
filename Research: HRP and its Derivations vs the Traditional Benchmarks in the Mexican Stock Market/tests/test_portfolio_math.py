import numpy as np

from src.portfolio_math import (
    portfolio_return,
    portfolio_variance,
    portfolio_volatility,
    global_minimum_variance,
    efficient_portfolio,
    efficient_frontier,
)

MU = np.array([0.08, 0.12, 0.05])

COV = np.array([
    [0.040, 0.012, 0.004],
    [0.012, 0.090, 0.006],
    [0.004, 0.006, 0.025]
])

# 1. Portfolio return
def test_portfolio_return():
    w = np.array([0.2, 0.3, 0.5])

    expected = 0.2 * 0.08 + 0.3 * 0.12 + 0.5 * 0.05

    result = portfolio_return(w, MU)

    assert np.isclose(result, expected)

# 2. Non-negative variance
def test_portfolio_variance_is_nonnegative():
    w = np.array([0.2, 0.3, 0.5])

    variance = portfolio_variance(w, COV)

    assert variance >= 0

# 3. Volatility = square root of variance
def test_portfolio_volatility_matches_variance():
    w = np.array([0.2, 0.3, 0.5])

    variance = portfolio_variance(w, COV)
    volatility = portfolio_volatility(w, COV)

    assert np.isclose(volatility, np.sqrt(variance))

# 4. GMV Portfolio weights add up to 1
def test_gmv_weights_sum_to_one():
    w = global_minimum_variance(COV)

    assert np.isclose(w.sum(), 1.0)

# 5. The GMV portfolio must have lower variance than arbitrary feasible portfolios
def test_gmv_has_lower_variance_than_example_portfolios():
    w_gmv = global_minimum_variance(COV)

    gmv_variance = portfolio_variance(w_gmv, COV)

    candidates = [
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([0.0, 0.0, 1.0]),
        np.array([1/3, 1/3, 1/3]),
        np.array([0.2, 0.3, 0.5]),
    ]

    for w in candidates:
        assert gmv_variance <= portfolio_variance(w, COV)

# 6. An efficient portfolio must satisfy the budget constraint.
def test_efficient_portfolio_weights_sum_to_one():
    target = 0.10

    w = efficient_portfolio(MU, COV, target)

    assert np.isclose(w.sum(), 1.0)

# 7. Efficient portfolio must achieve the target return
def test_efficient_portfolio_hits_target_return():
    target = 0.10

    w = efficient_portfolio(MU, COV, target)

    achieved_return = portfolio_return(w, MU)

    assert np.isclose(achieved_return, target)

# 8. Test different targets

def test_efficient_portfolio_multiple_targets():

    targets = np.linspace(0.07, 0.11, 10)

    for target in targets:

        w = efficient_portfolio(MU, COV, target)

        assert np.isclose(w.sum(), 1.0)
        assert np.isclose(w @ MU, target)
        assert portfolio_variance(w, COV) >= 0

# 9. The start of the efficient frontier must coincide with the GMV
def test_frontier_starts_at_gmv():

    risks, returns, weights = efficient_frontier(
        MU,
        COV,
        n_points=20
    )

    w_gmv = global_minimum_variance(COV)

    assert np.allclose(weights[0], w_gmv)