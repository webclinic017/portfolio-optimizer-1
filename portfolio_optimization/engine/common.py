from abc import abstractmethod
from typing import Dict, Optional

import numpy as np
import pandas as pd
from pypfopt import base_optimizer


class BaseOptimizer(base_optimizer.BaseOptimizer):
    expected_returns: pd.DataFrame
    cov_matrix: pd.DataFrame
    portfolios: Optional[pd.DataFrame]

    def describe_portfolio(self, n: Optional[int] = None) -> None:
        weights = self.get_clean_weights(n)
        self.portfolio_performance(portfolio_n=n)
        for asset, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
            print(f"{asset}: {weight}")

    def get_clean_weights(self, n: Optional[int] = None, rounding: int = 2) -> Dict:
        if n:
            w = self.get_portfolio_weights(n).copy()
            w[np.abs(w) < 1e-4] = 0
            w = np.round(w, rounding)
            return self._make_output_weights(w)

        return self.clean_weights(rounding=rounding)

    def get_portfolio(self, n: int) -> pd.DataFrame:
        return self.portfolios.loc[n]

    def max_sharpe(self) -> None:
        portfolio_n = self.portfolios["sharpe"].idxmax()
        portfolio = self.portfolios.iloc[portfolio_n]
        self.weights = np.asarray(portfolio.loc[[*self.tickers]])
        self._make_output_weights()

    def max_returns(self) -> None:
        portfolio_n = self.portfolios["ret"].idxmax()
        portfolio = self.portfolios.iloc[portfolio_n]
        self.weights = np.asarray(portfolio.loc[[*self.tickers]])
        self._make_output_weights()

    def min_volatility(self) -> None:
        portfolio_n = self.portfolios["volatility"].idxmin()
        portfolio = self.portfolios.iloc[portfolio_n]
        self.weights = np.asarray(portfolio.loc[[*self.tickers]])
        self._make_output_weights()

    def portfolio_performance(
        self,
        weights: Optional[np.array] = None,
        verbose: bool = True,
        risk_free_rate: float = 0.02,
        portfolio_n: Optional[int] = None,
    ):
        if portfolio_n:
            weights = self.get_portfolio_weights(portfolio_n)

        return base_optimizer.portfolio_performance(
            weights=weights if weights is not None else self.weights,
            expected_returns=self.expected_returns,  # type: ignore
            cov_matrix=self.cov_matrix,
            verbose=verbose,
            risk_free_rate=risk_free_rate,
        )

    def add_portfolio_performance_to_portfolios(
        self, portfolios: np.array, weights: np.array, i: int
    ) -> None:
        returns, volatility, sharpe = self.portfolio_performance(weights, verbose=False)
        portfolios[0, i] = returns
        portfolios[1, i] = volatility
        portfolios[2, i] = sharpe
        for j in range(len(weights)):
            portfolios[j + 3, i] = weights[j]

    @abstractmethod
    def get_portfolio_weights(self, n: int) -> np.array:
        ...
