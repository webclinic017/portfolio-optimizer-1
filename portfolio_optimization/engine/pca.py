from typing import Optional, Union

import numpy as np
import pandas as pd
from engine.common import BaseOptimizer
from sklearn.decomposition import PCA as PCA_


class PCAOptimizer(BaseOptimizer):
    def __init__(self, expected_returns: pd.DataFrame, cov_matrix: pd.DataFrame):
        self.expected_returns = expected_returns
        self.cov_matrix = cov_matrix
        self.portfolios: Optional[pd.DataFrame] = None
        self.pca = PCA_()
        self.pcs = self.pca.fit_transform(cov_matrix)
        tickers = list(expected_returns.index)
        super(PCAOptimizer, self).__init__(len(tickers), tickers)

    def generate_portfolios(self):
        portfolios = np.zeros((self.n_assets + 3, self.n_assets))

        for i in range(self.n_assets):
            weights = self._get_weights_from_component(i)
            self.add_portfolio_performance_to_portfolios(portfolios, weights, i)

        self.portfolios = pd.DataFrame(
            portfolios.T, columns=["ret", "volatility", "sharpe", *self.tickers]
        )

    def get_portfolio_weights(self, n: int) -> np.array:
        return self._get_weights_from_component(n)

    def _get_weights_from_component(
        self, component: Union[np.ndarray, int]
    ) -> np.array:
        if isinstance(component, int):
            component = self.pcs[component]

        return abs(component) / sum(abs(component))
