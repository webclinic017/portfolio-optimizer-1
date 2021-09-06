from typing import Iterable, List, Union

import pandas as pd
import yfinance as yf
from pypfopt import CLA, EfficientFrontier, HRPOpt, expected_returns, risk_models

from portfolio_optimization.cache import use_requests_cache
from portfolio_optimization.engine.optimizers.monte_carlo import MonteCarloOptimizer
from portfolio_optimization.engine.optimizers.pca import PCAOptimizer
from portfolio_optimization.models import (
    OptimizationResults,
    Optimizer,
    ReturnModel,
    RiskModel,
    Target,
)

BASE_OPTIMIZERS_MAP = {
    Optimizer.mc: MonteCarloOptimizer,
    Optimizer.pca: PCAOptimizer,
    Optimizer.cla: CLA,
    Optimizer.ef: EfficientFrontier,
}


@use_requests_cache()
def get_daily_data_for_tickers(
    tickers: Iterable[str], ffill: bool = True, dropna: bool = True
) -> pd.DataFrame:
    data: pd.DataFrame = yf.download(
        " ".join(tickers),
        period="max",
        interval="1d",
        group_by="ticker",
        threads=False,
        progress=False,
        show_errors=False,
    )

    if wrong_tickers := [t for t in tickers if not data[t.upper()].any().values.any()]:
        raise ValueError(
            f"No data found for {', '.join(wrong_tickers)}. Symbol(s) may be delisted or incorrect.",
        )

    if ffill:
        data = data.ffill()

    if dropna:
        data = data.dropna()

    return data


def get_adj_close_daily_data_for_tickers(tickers: Iterable[str]) -> pd.DataFrame:
    return (
        get_daily_data_for_tickers(tickers)
        .stack(level=0)
        .rename_axis(["Date", "Ticker"])
        .unstack(level=1)["Adj Close"]
    )


def optimize(
    tickers: List[str],
    optimizer: Optimizer = Optimizer.ef,
    risk_model: RiskModel = RiskModel.oracle_approximating,
    return_model: ReturnModel = ReturnModel.capm_return,
    target: Target = Target.max_sharpe,
) -> OptimizationResults:
    # prices
    df_prices: pd.DataFrame = get_adj_close_daily_data_for_tickers(tickers)

    # model
    model: Union[HRPOpt, MonteCarloOptimizer, PCAOptimizer, CLA, EfficientFrontier]
    if optimizer == Optimizer.hrp:
        model = HRPOpt(expected_returns.returns_from_prices(df_prices))
        model.optimize()
    else:
        mu: pd.DataFrame = expected_returns.return_model(
            df_prices, method=return_model.value, frequency=365
        )
        S: pd.DataFrame = risk_models.risk_matrix(
            df_prices, frequency=365, method=risk_model.value
        )
        model = BASE_OPTIMIZERS_MAP[optimizer](mu, S)
        actual_optimization_method = getattr(model, target.value)
        actual_optimization_method()

    # weights
    weights = model.clean_weights(rounding=2)

    # performance
    (
        expected_annual_return,
        annual_volatility,
        sharpe_ratio,
    ) = model.portfolio_performance()

    return OptimizationResults(
        optimizer=optimizer.value,
        risk_model=risk_model.value,
        return_model=return_model.value,
        weights=weights,
        expected_annual_return=expected_annual_return * 100,
        annual_volatility=annual_volatility * 100,
        sharpe_ratio=sharpe_ratio,
    )
