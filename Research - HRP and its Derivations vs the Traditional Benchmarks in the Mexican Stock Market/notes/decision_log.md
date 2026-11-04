##  
- **Date:** 2026-11-02
- **Status:** Pending
- **Question:** What time window ($T$) and data frequency should be used to estimate the covariance matrix ($\Sigma$) in the backtest?

- **Evidence:**

- The relevant metric is the spectral noise intensity $q = N/T$ (where $N=35$ assets and $T$ represents the number of observations). If $q \to 0$, the estimate is robust; however, if $q \geq 1$, one encounters the "curse of dimensionality," and the sample matrix $S$ is no longer invertible. 

- **Monthly Window ($T = 60$, 5 years):** Exhibits high noise, with $q \approx 0.583$. It significantly underestimates the minimum eigenvalue ($\lambda(S)_{\min} / \lambda_{\min} = 0.6591$) and causes the condition number to spike to $\kappa(S) \approx 364$ (8.4 times higher than the actual value, $\kappa(\Sigma) = 43.2417$). 

- **Daily Window ($T = 250$, approx. 1 year):** Significantly reduces noise, with $q = 0.14$. The underestimation of $\lambda_{\min}$ is much smaller ($\lambda(S)_{\min} / \lambda_{\min} = 0.9060$), and the condition number stabilizes at $\kappa(S) \approx 66$ (only 1.5 times the actual value). As $T$ increases, the matrix becomes better conditioned (a downward trend observed in simulations ranging from $T=40$ to $T=5000$). 

- **Alternatives:**
- **5-year monthly ($T=60$):** Fewer observations, higher spectral noise, but potentially capable of capturing longer-term macro dynamics. 
- **1-year daily ($T=250$):** Larger dataset, lower sampling noise, and a numerically more robust estimation.
- **Shrinkage Estimator:** Ledoit-Wolf.

- **Implications:**

- **For GMV (Global Minimum Variance):** Since this portfolio relies on $S^{-1}$ (where eigenvalues ​​are $1/\lambda$), underestimating $\lambda_{\min}$—as happens with $T=60$—leads the optimizer to falsely identify that direction as much less risky than it actually is, resulting in excessive and unrealistic weight allocations. The daily window ($T=250$) mitigates this error. 

- **For Hierarchical Methods:** Because the matrix is ​​better conditioned when using daily data ($\kappa(S) \approx 66$), the distances and dependency structures utilized by hierarchical clustering algorithms become more stable against numerical perturbations. 

- **Limitations not captured by the simulation:** The simulation assumes i.i.d. normal returns and a static $\Sigma$. In reality, a 5-year window risks conflating outdated market regimes, while daily data for illiquid assets tends to underestimate correlations and exhibit heavy tails.

- **Decision / Next Steps:** **Pending.** Statistical evidence regarding noise favors the daily window ($T=250$). However, the final decision remains contingent upon evaluating the impact of the non-stationarity of $\Sigma$ over time, as well as the fact that real-world returns do not follow an i.i.d. normal distribution.