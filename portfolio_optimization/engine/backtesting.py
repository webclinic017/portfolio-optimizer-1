from typing import Dict

import bt
import pandas as pd


class Backtesting:
    def __init__(self, prices_df: pd.DataFrame, add_raw_tickers: bool = True) -> None:
        self.prices_df = prices_df
        self.strategies = []

        if add_raw_tickers:
            for t in prices_df.columns:
                self.add_strategy(
                    weights={
                        **{tk: 0.0 for tk in prices_df.columns if tk != t},
                        t: 1.0,
                    },
                    name=t,
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
                progress_bar=False,
                integer_positions=False,
            )
        )

    def run(self) -> bt.backtest.Result:
        return bt.run(*self.strategies)
