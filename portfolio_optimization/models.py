from enum import Enum
from typing import Dict

from pydantic import BaseModel, Field


class Optimizer(str, Enum):
    hrp = "hrp"
    mc = "mc"
    pca = "pca"
    cla = "cla"
    ef = "ef"


class RiskModel(str, Enum):
    sample_cov = "sample_cov"
    semicovariance = "semicovariance"
    exp_cov = "exp_cov"
    ledoit_wolf = "ledoit_wolf"
    ledoit_wolf_constant_variance = "ledoit_wolf_constant_variance"
    ledoit_wolf_single_factor = "ledoit_wolf_single_factor"
    ledoit_wolf_constant_correlation = "ledoit_wolf_constant_correlation"
    oracle_approximating = "oracle_approximating"


class Target(str, Enum):
    max_sharpe = "max_sharpe"
    min_volatility = "min_volatility"


class ReturnModel(str, Enum):
    mean_historical_return = "mean_historical_return"
    ema_historical_return = "ema_historical_return"
    capm_return = "capm_return"


class OptimizationResults(BaseModel):
    optimizer: Optimizer = Field(
        ..., description="Optimizer used to solve the optimization problem."
    )
    risk_model: RiskModel = Field(..., description="Risk model used.")
    return_model: ReturnModel = Field(
        ...,
        description="Return model used to calculate an estimate of future returns. Doesn't matter if `hrp` is chosen as an optimizer.",
    )
    weights: Dict[str, float] = Field(
        ...,
        description="JSON-like object containing `asset: proportion of investments` which corresponds the solved problem results.",
    )
    expected_annual_return: float = Field(
        ..., description="Expected annual return (%)."
    )
    annual_volatility: float = Field(..., description="Annual volatility (%).")
    sharpe_ratio: float = Field(..., description="Sharpe ratio.")
