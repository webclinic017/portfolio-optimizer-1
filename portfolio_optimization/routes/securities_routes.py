from typing import List

from controller import crypto_controller
from fastapi import APIRouter

securities_router = APIRouter(prefix="/securities/v1", tags=["securities"])


@securities_router.get("/crypto")
async def get_top_crypto_coins(n: int = 50) -> List[str]:
    return await crypto_controller.get_top_coins(n=n)
