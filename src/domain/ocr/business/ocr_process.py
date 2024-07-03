from io import BytesIO
from itertools import groupby

from fastapi import BackgroundTasks
from PIL import Image

from src.dependency import ports
from src.domain.user.model import user_request

from ..converter import ocr_converter
from ..model import ocr_model, ocr_response
from ..model.enums import ocr_enum
from ..service import image_logic, ocr_logic


async def run_image_ocr(
    *,
    background_tasks: BackgroundTasks,
    user: user_request.UserCurrent,
    meta_repo: ports.OcrMetaRepository,
    image_repo: ports.ImageRepository,
    ocr_repo: ports.OcrRepository,
    inferencer: ports.OcrInferencer,
    image_id: int,
    data: list[ocr_model.Roi],
    lang: list[ocr_enum.OcrLangEnum],
    psm: int,
    oem: int,
) -> list[ocr_model.OcrResultBase]:
    image_entity = await image_logic.get_image_meta(
        repo=meta_repo,
        image_id=image_id,
    )
    image_data = await image_logic.get_image(repo=image_repo, metadata=image_entity)
    src_image = Image.open(fp=BytesIO(image_data))
    ocr_result = await ocr_logic.run_image_ocr(
        inferencer=inferencer,
        image=src_image,
        roi_list=data,
        lang=lang,
        psm=psm,
        oem=oem,
    )
    background_tasks.add_task(
        ocr_logic.save_ocr_result,
        meta_repo=meta_repo,
        ocr_repo=ocr_repo,
        current_user=user,
        ocr_result=ocr_result,
        meta_data=image_entity,
    )
    return ocr_result


async def get_ocr_result(
    *,
    meta_repo: ports.OcrMetaRepository,
    ocr_repo: ports.OcrRepository,
    image_id: int,
    version: int | None,
) -> list[ocr_response.OcrResultResponse]:
    ocr_result_meta = await ocr_logic.get_ocr_result_meta(
        repo=meta_repo,
        image_id=image_id,
        version=version,
    )

    grouped_data = {
        key: [
            await ocr_converter.to_OcrResult(
                ocr_result=await ocr_repo.read_result_by_content_id(
                    content_id=v.content_id
                )
            )
            for v in value
        ]
        for key, value in groupby(
            iterable=ocr_result_meta,
            key=lambda x: ocr_model.OcrResultMeta(
                version=x.version,
                created_datetime=x.created_datetime,
            ),
        )
    }

    res = [
        ocr_response.OcrResultResponse(
            version=key.version,
            created_datetime=key.created_datetime,
            contents=value,
        )
        for key, value in grouped_data.items()
    ]
    return res


async def update_ocr(
    *,
    current_user: user_request.UserCurrent,
    meta_repo: ports.OcrMetaRepository,
    user_repo: ports.UserRepository,
    ocr_repo: ports.OcrRepository,
    content_id: str,
    data: ocr_model.OcrResultBase,
) -> None:
    await ocr_logic.verify_authority(
        meta_repo=meta_repo,
        user_repo=user_repo,
        current_user=current_user,
        content_id=content_id,
    )
    await ocr_logic.update_ocr_result(repo=ocr_repo, content_id=content_id, data=data)


async def delete_ocr(
    *,
    current_user: user_request.UserCurrent,
    meta_repo: ports.OcrMetaRepository,
    user_repo: ports.UserRepository,
    ocr_repo: ports.OcrRepository,
    content_id: str,
) -> None:
    await ocr_logic.verify_authority(
        meta_repo=meta_repo,
        user_repo=user_repo,
        current_user=current_user,
        content_id=content_id,
    )
    await ocr_logic.delete_ocr_result(
        meta_repo=meta_repo,
        ocr_repo=ocr_repo,
        content_id=content_id,
    )
