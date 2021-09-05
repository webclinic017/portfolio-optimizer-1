from fastapi import FastAPI

from portfolio_optimization.routes.api_routes import api_router

DESCRIPTION = """
Portfolio Optimizer API based on [PyPortfolioOpt](https://pyportfolioopt.readthedocs.io/en/latest/) and [FastAPI](http://fastapi.tiangolo.com/) libraries.

## Tickers
Tickers can be found at [Yahoo Finance](https://finance.yahoo.com).

## Optimizers
* **hrp** - Hierarchical Risk Parity
* **mc** - Monte Carlo
* **pca** - Principal Component Analysis
* **cla** - Critical Line Algorithm by Marcos Lopez de Prado and David Bailey
* **ef** - Efficient Frontier (classical mean-variance)

## Risk Models
* **sample_cov** - Sample Covariance Matrix of asset returns
* **semicovariance** - Semicovariance Matrix, i.e the covariance given that the returns are less than the benchmark
* **exp_cov** - Exponentially-weighted covariance matrix, which gives greater weight to more recent data
* **ledoit_wolf** - Ledoit-Wolf shrinkage estimate
* **ledoit_wolf_constant_variance** - Ledoit-Wolf shrinkage estimate for a constant variance
* **ledoit_wolf_single_factor** - Ledoit-Wolf shrinkage estimate for a single factor
* **ledoit_wolf_constant_correlation** - Ledoit-Wolf shrinkage estimate for a constant correlation
* **oracle_approximating** - Oracle Approximating Shrinkage estimate
"""


def create_app(testing: bool = False) -> FastAPI:
    app = FastAPI(
        debug=testing,
        title="Portfolio Optimization",
        description=DESCRIPTION,
        contact={"name": "Eugene Serdyuk", "email": "eugene.serdyuk@pm.me"},
        version="0.1.0",
    )

    app.include_router(api_router)

    return app
