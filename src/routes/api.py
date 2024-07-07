from fastapi import APIRouter

from src.domain.ocr.endpoint import image_controller, ocr_controller
from src.domain.user.endpoint import user_controller

from .enums.tag import RouterTagEnum

router = APIRouter(prefix="/v1")

router.include_router(
    router=user_controller.router,
    tags=[RouterTagEnum.USER],
)

router.include_router(
    router=image_controller.router,
    tags=[RouterTagEnum.OCR],
)

router.include_router(
    router=ocr_controller.router,
    tags=[RouterTagEnum.OCR],
)
