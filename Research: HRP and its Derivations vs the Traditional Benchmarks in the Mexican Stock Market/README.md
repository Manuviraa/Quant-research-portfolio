# HRP / HERC / NCO vs Traditional Portfolio Allocation in the Mexican Equity Market

## Project Overview

This project studies whether hierarchical portfolio allocation methods
such as Hierarchical Risk Parity (HRP), Hierarchical Equal Risk Contribution
(HERC), and Nested Clustered Optimization (NCO) produce more robust
out-of-sample portfolios than traditional allocation methods in the
Mexican equity market.

The final study will compare:

- Equal Weight (1/N)
- Market-Cap Weight
- Global Minimum Variance
- Mean-Variance Optimization
- HRP
- HERC
- NCO

The investment universe will be based on the historical composition
of the S&P/BMV IPC, using time-consistent index membership to avoid
survivorship and look-ahead bias.

---

## Current Stage

### Week 1 — Markowitz Foundations

The objective of Week 1 was to derive and implement the foundations
of classical portfolio optimization from first principles before
introducing portfolio-optimization libraries.

Topics covered:

- Budget and long-only constraints
- Dimensionality reduction of a three-asset portfolio
- Iso-mean curves
- Iso-variance curves
- Portfolio return and variance
- Monte Carlo portfolio generation
- Global Minimum Variance portfolio
- Analytical efficient frontier
- Estimation error
- Eigenvalues, eigendecomposition and covariance conditioning
- 1/N as an out-of-sample benchmark

---

## Mathematical Foundations

Portfolio expected return:

$$
E[R_p] = w^\top \mu
$$

Portfolio variance:

$$
\sigma_p^2 = w^\top \Sigma w
$$

Global Minimum Variance portfolio:

$$
w_{GMV}
=
\frac{\Sigma^{-1}\mathbf{1}}
{\mathbf{1}^\top\Sigma^{-1}\mathbf{1}}
$$

For a target return \(r^*\), the minimum-variance portfolio satisfies:

$$
w
=
\Sigma^{-1}A
(A^\top\Sigma^{-1}A)^{-1}b
$$

where

$$
A=
\begin{bmatrix}
\mathbf{1} & \mu
\end{bmatrix},
\qquad
b=
\begin{bmatrix}
1\\
r^*
\end{bmatrix}.
$$

---

## Week 1 Experiments

A synthetic three-asset covariance matrix was used to study the
geometry of Markowitz portfolios.

50,000 long-only portfolios were generated using random weights
satisfying:

$$
w_i \ge 0,
\qquad
\sum_i w_i = 1.
$$

The analytical GMV portfolio was compared with the lowest-variance
portfolio found through Monte Carlo simulation.

A covariance stress test was also performed by progressively increasing
the correlation between two assets. As the smallest eigenvalue approached
zero, the condition number increased substantially and the unconstrained
GMV weights became increasingly extreme.

This illustrates an important distinction:

> A mathematically exact optimizer can still be a statistically unstable estimator.

---

## Important Methodological Note

The Monte Carlo portfolio cloud generated in Week 1 is long-only.

The analytical efficient frontier currently implemented does not impose
non-negativity constraints and therefore allows short selling.

The displayed analytical frontier is truncated at the highest individual
asset expected return for visualization; mathematically, the unconstrained
frontier can extend beyond that return.

---

## Repository Structure

```text
figures/      Generated research figures
notebooks/    Research and pedagogical notebooks
notes/        Mathematical derivations and reading notes
src/          Reusable portfolio functions
tests/        Unit tests for mathematical functions
```

## Reproducibility
The Monte Carlo experiments use fixed random seeds where applicable.
The portfolio optimization functions are implemented from first
principles using NumPy. Portfolio-specific optimization libraries are
intentionally avoided during the foundational stage of the project.
Run the tests with pytest

## What I Derived
- Three-asset expected-return equation after dimensionality reduction
- Quadratic form of portfolio variance
- Global Minimum Variance portfolio
- Minimum-variance portfolio subject to a target expected return

# What I Implemented
- Portfolio expected return
- Portfolio variance
- Portfolio volatility
- Global Minimum Variance allocation
- Efficient portfolio for a target return
- Efficient frontier
- Monte Carlo portfolio simulation
- Covariance conditioning stress test