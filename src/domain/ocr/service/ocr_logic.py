from datetime import datetime
from typing import Sequence

from fastapi import HTTPException
from PIL import Image
from starlette import status

from src.core import auth
from src.core.configs import KST
from src.core.exception import QueryResultEmptyError
from src.db.entity import ocr_entity
from src.dependency import ports
from src.domain.user.model import user_request

from ..model import ocr_model
from ..model.enums import ocr_enum


async def run_image_ocr(
    *,
    inferencer: ports.OcrInferencer,
    image: Image.Image,
    roi_list: list[ocr_model.Roi],
    lang: list[ocr_enum.OcrLangEnum],
    psm: int,
    oem: int,
) -> list[ocr_model.OcrResultBase]:
    res = [
        ocr_model.OcrResultBase(
            roi=roi,
            detail=await inferencer.extract_text(
                image=image,
                roi=roi,
                lang="+".join(lang),
                config=rf"--oem {oem} --psm {psm}",
            ),
        )
        for roi in roi_list
    ]
    return res


async def save_ocr_result(
    *,
    meta_repo: ports.OcrMetaRepository,
    ocr_repo: ports.OcrRepository,
    current_user: user_request.UserCurrent,
    ocr_result: list[ocr_model.OcrResultBase],
    meta_data: ocr_entity.ImageEntity,
) -> None:
    mongo_res = await ocr_repo.create_ocr_result(
        doc=[v.model_dump() for v in ocr_result]
    )
    version = await meta_repo.read_ocr_last_version(image_id=meta_data.id)
    await meta_repo.create_ocr_result_meta(
        version=version + 1 if version else 1,
        created_datetime=datetime.now(KST),
        image_id=meta_data.id,
        user_id=current_user.id,
        content_ids=mongo_res,
    )


async def get_ocr_result_meta(
    *,
    repo: ports.OcrMetaRepository,
    image_id: int,
    version: int | None,
) -> Sequence[ocr_entity.OcrEntity]:
    ocr_result = await repo.read_ocr_result_meta(image_id=image_id, version=version)
    if not ocr_result:
        raise QueryResultEmptyError
    return ocr_result


async def verify_authority(
    *,
    meta_repo: ports.OcrMetaRepository,
    user_repo: ports.UserRepository,
    current_user: user_request.UserCurrent,
    content_id: str,
) -> None:
    ocr_meta = await meta_repo.read_result_by_content_id(content_id=content_id)
    role_entity = await user_repo.read_user_role(user_id=current_user.id)
    if not ocr_meta:
        raise QueryResultEmptyError
    elif not any(
        [
            ocr_meta.user_id != current_user.id,
            await auth.verify_admin(role=role_entity),
        ]
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="you are not authorized",
        )


async def update_ocr_result(
    *,
    repo: ports.OcrRepository,
    content_id: str,
    data: ocr_model.OcrResultBase,
) -> None:
    await repo.update_ocr_result(content_id=content_id, data=data)


async def delete_ocr_result(
    *,
    meta_repo: ports.OcrMetaRepository,
    ocr_repo: ports.OcrRepository,
    content_id: str,
) -> None:
    await meta_repo.delete_ocr_meta(content_id=content_id)
    await ocr_repo.delete_ocr_result(content_id=content_id)
