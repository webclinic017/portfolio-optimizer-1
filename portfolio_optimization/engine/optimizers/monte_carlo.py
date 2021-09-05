from typing import Optional

import numpy as np
import pandas as pd

from portfolio_optimization.engine.optimizers.common import BaseOptimizer


class MonteCarloOptimizer(BaseOptimizer):
    def __init__(
        self,
        expected_returns: pd.Series,
        cov_matrix: pd.DataFrame,
        n_portfolios: int = 1000,
    ):
        self.expected_returns = expected_returns
        self.cov_matrix = cov_matrix
        self.portfolios: Optional[pd.DataFrame] = None
        self.n_portfolios = n_portfolios
        tickers = list(expected_returns.index)
        super(MonteCarloOptimizer, self).__init__(len(tickers), tickers)
        self.generate_portfolios()

    def generate_portfolios(self, n_portfolios: Optional[int] = None):
        n_portfolios = n_portfolios if n_portfolios else self.n_portfolios
        portfolios = np.zeros((self.n_assets + 3, n_portfolios))

        for i in range(n_portfolios):
            weights = self.get_random_weights()
            self.add_portfolio_performance_to_portfolios(portfolios, weights, i)

        self.portfolios = pd.DataFrame(
            portfolios.T, columns=["ret", "volatility", "sharpe", *self.tickers]
        )

    def get_random_weights(self):
        weights = np.random.rand(self.n_assets)
        return weights / np.sum(weights)

    def get_portfolio_weights(self, n: int) -> np.array:
        return self.portfolios.iloc[n].drop(["ret", "volatility", "sharpe"]).to_numpy()
