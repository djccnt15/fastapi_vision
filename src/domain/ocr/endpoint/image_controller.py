from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends, Path, Query
from fastapi.datastructures import UploadFile
from fastapi.responses import Response
from starlette import status

from src import dependency
from src.core import auth
from src.core.model.enums import ResponseEnum

from ..business import image_process, ocr_process
from ..model import ocr_model, ocr_request, ocr_response
from ..model.enums import ocr_enum

router = APIRouter(prefix="/image")


@router.post(path="", status_code=status.HTTP_201_CREATED)
async def upload_image(
    current_user: auth.CurrentUser,
    meta_repo: dependency.MetaRepo,
    image_repo: dependency.ImageRepo,
    file: UploadFile,
) -> ResponseEnum:
    await image_process.upload_image(
        user=current_user,
        meta_repo=meta_repo,
        image_repo=image_repo,
        file=file,
    )
    return ResponseEnum.CREATE


@router.get(path="")
async def get_image_list(
    repo: dependency.MetaRepo,
    keyword: Annotated[str | None, Query()] = None,
    size: Annotated[int, Query(gt=0)] = 10,
    page: Annotated[int, Query(ge=0)] = 0,
) -> list[ocr_response.ImageResponse]:
    res = await image_process.get_image_list(
        repo=repo,
        keyword=keyword,
        size=size,
        page=page,
    )
    return res


@router.get(path="/{id}", dependencies=[Depends(auth.get_current_user)])
async def get_image(
    meta_repo: dependency.MetaRepo,
    image_repo: dependency.ImageRepo,
    id: Annotated[int, Path(gt=0)],
) -> Response:
    res = await image_process.get_image(
        meta_repo=meta_repo,
        image_repo=image_repo,
        image_id=id,
    )
    return res


@router.get(path="/{id}/thumbnail", dependencies=[Depends(auth.get_current_user)])
async def get_thumbnail(
    meta_repo: dependency.MetaRepo,
    image_repo: dependency.ImageRepo,
    id: Annotated[int, Path(gt=0)],
) -> Response:
    res = await image_process.get_thumbnail(
        meta_repo=meta_repo,
        image_repo=image_repo,
        image_id=id,
    )
    return res


@router.put(path="/{id}")
async def update_image(
    current_user: auth.CurrentUser,
    meta_repo: dependency.MetaRepo,
    image_repo: dependency.ImageRepo,
    id: Annotated[int, Path(gt=0)],
    body: Annotated[ocr_request.ImageUpdateRequest, Body()],
) -> ResponseEnum:
    await image_process.update_image(
        user=current_user,
        meta_repo=meta_repo,
        image_repo=image_repo,
        image_id=id,
        data=body,
    )
    return ResponseEnum.UPDATE


@router.delete(path="/{id}")
async def delete_image(
    current_user: auth.CurrentUser,
    meta_repo: dependency.MetaRepo,
    image_repo: dependency.ImageRepo,
    id: Annotated[int, Path(gt=0)],
) -> ResponseEnum:
    await image_process.delete_image(
        user=current_user,
        meta_repo=meta_repo,
        image_repo=image_repo,
        image_id=id,
    )
    return ResponseEnum.DELETE


@router.post(path="/{id}/ocr")
async def run_image_ocr(
    background_tasks: BackgroundTasks,
    current_user: auth.CurrentUser,
    meta_repo: dependency.MetaRepo,
    image_repo: dependency.ImageRepo,
    ocr_repo: dependency.OcrRepo,
    inferencer: dependency.OcrInferencer,
    id: Annotated[int, Path(gt=0)],
    body: Annotated[list[ocr_model.Roi], Body()],
    lang: Annotated[list[ocr_enum.OcrLangEnum], Query()] = [ocr_enum.OcrLangEnum.ENG],
    psm: Annotated[int, Query(gt=0)] = 3,
    oem: Annotated[int, Query(gt=0)] = 3,
) -> list[ocr_model.OcrResultBase]:
    res = await ocr_process.run_image_ocr(
        background_tasks=background_tasks,
        meta_repo=meta_repo,
        image_repo=image_repo,
        ocr_repo=ocr_repo,
        inferencer=inferencer,
        user=current_user,
        image_id=id,
        lang=lang,
        psm=psm,
        oem=oem,
        data=body,
    )
    return res


@router.get(path="/{id}/ocr")
async def get_ocr_result(
    meta_repo: dependency.MetaRepo,
    ocr_repo: dependency.OcrRepo,
    id: Annotated[int, Path(gt=0)],
    version: Annotated[int | None, Query(gt=0)] = 0,
) -> list[ocr_response.OcrResultResponse]:
    res = await ocr_process.get_ocr_result(
        meta_repo=meta_repo,
        ocr_repo=ocr_repo,
        image_id=id,
        version=version,
    )
    return res
