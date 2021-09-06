# Portfolio Optimization

Portfolio Optimizer API based on [PyPortfolioOpt](https://pyportfolioopt.readthedocs.io/en/latest/)
and [FastAPI](http://fastapi.tiangolo.com/) libraries.

- [Swagger](https://eserdk-portfolio-optimization.herokuapp.com/docs)
- [ReDoc](https://eserdk-portfolio-optimization.herokuapp.com/redoc)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f16b330768264649b74cbad4c8532860)](https://www.codacy.com/gh/eserdk/portfolio-optimization/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=eserdk/portfolio-optimization&amp;utm_campaign=Badge_Grade)

***

## API

### Tickers

Tickers can be found at [Yahoo Finance](https://finance.yahoo.com).

### Optimizers

- **hrp** Hierarchical Risk Parity
- **mc** Monte Carlo
- **pca** Principal Component Analysis
- **cla** Critical Line Algorithm by Marcos Lopez de Prado and David Bailey
- **ef** Efficient Frontier (classical mean-variance)

### Risk Models

- **sample_cov** Sample Covariance Matrix of asset returns
- **semicovariance** Semicovariance Matrix, i.e the covariance given that the returns are less than the benchmark
- **exp_cov** Exponentially-weighted covariance matrix, which gives greater weight to more recent data
- **ledoit_wolf** Ledoit-Wolf shrinkage estimate
- **ledoit_wolf_constant_variance** Ledoit-Wolf shrinkage estimate for a constant variance
- **ledoit_wolf_single_factor** Ledoit-Wolf shrinkage estimate for a single factor
- **ledoit_wolf_constant_correlation** Ledoit-Wolf shrinkage estimate for a constant correlation
- **oracle_approximating** Oracle Approximating Shrinkage estimate

### Return Models

- **mean_historical_return** Annualised mean (daily) historical return from input (daily) asset prices
- **ema_historical_return** Exponentially-weighted mean of (daily) historical returns, giving higher weight to more
  recent data
- **capm_return** Capital Asset Pricing Model: under the CAPM, asset returns are equal to market returns plus a beta term encoding the relative risk of the asset

### Target

- **max_sharpe** Maximize Sharpe ratio
- **min_volatility** Minimize volatility  
