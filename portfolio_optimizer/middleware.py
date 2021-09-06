import time
from typing import Callable

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response


async def add_process_time_header(request: Request, call_next: Callable) -> Response:
    start_time = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time-Seconds"] = str(time.time() - start_time)
    return response


def add_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=(
            "http://localhost",
            "http://0.0.0.0",
            "https://eserdk-portfolio-optimization.herokuapp.com",
        ),
        allow_methods=("*",),
    )

    app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
