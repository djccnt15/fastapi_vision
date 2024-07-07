from fastapi import APIRouter

from src.domain.default.controller import default_endpoint

from .enums import tag

router = APIRouter()

router.include_router(
    router=default_endpoint.router,
    tags=[tag.RouterTagEnum.DEFAULT],
)
