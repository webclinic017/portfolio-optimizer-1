from typing import List

import fastapi.exceptions
from fastapi import APIRouter, Query

from portfolio_optimization import controller
from portfolio_optimization.models import (
    OptimizationResults,
    Optimizer,
    RiskModel,
    Target,
)

api_router = APIRouter(prefix="/api", tags=["api"])


@api_router.post(
    "/v1/optimize",
    response_model=OptimizationResults,
    status_code=200,
    description="Calculate optimal weights for the given tickers (in request body), optimizer, risk model and target.",
)
def optimize(
    tickers: List[str],
    optimizer: Optimizer = Query(Optimizer.ef, description="Optimizer to use."),
    risk_model: RiskModel = Query(
        RiskModel.oracle_approximating, description="Risk model to use."
    ),
    target: Target = Query(
        Target.max_sharpe,
        description="Optimization problem to solve. Doesn't matter if `hrp` is chosen as an optimizer.",
    ),
) -> OptimizationResults:
    try:
        return controller.optimize(
            tickers=tickers,
            optimizer=optimizer,
            risk_model=risk_model,
            target=target,
        )
    except ValueError as e:
        raise fastapi.exceptions.HTTPException(404, str(e))
