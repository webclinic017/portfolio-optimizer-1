from fastapi import FastAPI

from portfolio_optimization.routes.api_routes import api_router


def create_app(testing: bool = False) -> FastAPI:
    app = FastAPI(
        debug=testing,
        title="Portfolio Optimization",
        version="0.1.0",
    )

    app.include_router(api_router)

    return app
