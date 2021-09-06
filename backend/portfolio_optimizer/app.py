from pathlib import Path

from fastapi import FastAPI

from portfolio_optimizer.middleware import add_middleware
from portfolio_optimizer.routes.api_routes import api_router


def create_app(testing: bool = False) -> FastAPI:
    app = FastAPI(
        debug=testing,
        title="Portfolio Optimization",
        description=(Path(__file__).parent.parent.parent / "README.md").read_text(),
        contact={"name": "Eugene Serdyuk", "email": "eugene.serdyuk@pm.me"},
        version="0.1.0",
    )

    add_middleware(app)

    app.include_router(api_router)

    return app
