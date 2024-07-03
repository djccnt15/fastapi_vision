from typing import Annotated

from fastapi import APIRouter, Body, Path
from fastapi.responses import JSONResponse

from src import dependency
from src.core import auth
from src.core.model.enums import ResponseEnum

from ..business import ocr_process
from ..model import ocr_model, ocr_response
from ..model.enums import ocr_enum

router = APIRouter(prefix="/ocr")


@router.put(path="/{id}")
async def update_ocr(
    current_user: auth.CurrentUser,
    meta_repo: dependency.MetaRepo,
    user_repo: dependency.UserRepo,
    ocr_repo: dependency.OcrRepo,
    id: Annotated[str, Path(gt=0)],
    body: Annotated[ocr_model.OcrResultBase, Body()],
) -> ResponseEnum:
    await ocr_process.update_ocr(
        current_user=current_user,
        meta_repo=meta_repo,
        user_repo=user_repo,
        ocr_repo=ocr_repo,
        content_id=id,
        data=body,
    )
    return ResponseEnum.UPDATE


@router.delete(path="/{id}")
async def delete_ocr(
    current_user: auth.CurrentUser,
    meta_repo: dependency.MetaRepo,
    user_repo: dependency.UserRepo,
    ocr_repo: dependency.OcrRepo,
    id: Annotated[str, Path()],
) -> ResponseEnum:
    await ocr_process.delete_ocr(
        current_user=current_user,
        meta_repo=meta_repo,
        user_repo=user_repo,
        ocr_repo=ocr_repo,
        content_id=id,
    )
    return ResponseEnum.DELETE


@router.get(path="/psm")
async def get_psm_list() -> JSONResponse:
    return JSONResponse(content=ocr_response.PSM_LIST)


@router.get(path="/oem")
async def get_oem_list() -> JSONResponse:
    return JSONResponse(content=ocr_response.OEM_LIST)


@router.get(path="/lang")
async def get_lang_list() -> list[str]:
    return ocr_enum.OcrLangEnum.to_list()
