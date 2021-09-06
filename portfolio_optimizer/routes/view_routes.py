from fastapi import APIRouter
from starlette.responses import RedirectResponse

view_router = APIRouter(tags=["view"])


@view_router.get(
    "/",
    responses={307: {"description": "Redirects to `/docs`"}},
    response_class=RedirectResponse,
)
def serve_index() -> RedirectResponse:
    return RedirectResponse(url="/docs")
