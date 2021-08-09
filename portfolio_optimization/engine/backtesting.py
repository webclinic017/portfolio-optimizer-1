from typing import Dict, List

import bt
import pandas as pd


class Backtesting:
    def __init__(self, prices_df: pd.DataFrame, add_raw_tickers: bool = True) -> None:
        self.prices_df = prices_df
        self.strategies = []

        if add_raw_tickers:
            cols: List = list(prices_df.columns)
            for t in cols:
                self.add_strategy(
                    weights={**{tk: 0.0 for tk in cols if tk != t}, **{t: 1.0}}, name=t
                )

    def add_strategy(self, weights: Dict, name: str) -> None:
        self.strategies.append(
            bt.Backtest(
                strategy=bt.Strategy(
                    name,
                    algos=[
                        bt.algos.RunOnce(),
                        bt.algos.SelectAll(),
                        bt.algos.WeighSpecified(**weights),
                        bt.algos.Rebalance(),
                    ],
                ),
                data=self.prices_df,
                initial_capital=1.0,
                commissions=lambda quantity, price: (quantity * price) * 0.001,
                progress_bar=False,
                integer_positions=False,
            )
        )

    def run(self) -> bt.backtest.Result:
        return bt.run(*self.strategies)
