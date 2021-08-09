from fastapi import FastAPI
from routes import securities_routes

from portfolio_optimization.client import coingecko_client


def create_app(testing: bool = False) -> FastAPI:
    app = FastAPI(
        debug=testing,
        title="Portfolio Optimization",
        version="0.1.0",
        on_shutdown=[coingecko_client.close],
    )

    app.include_router(securities_routes.securities_router)

    return app
