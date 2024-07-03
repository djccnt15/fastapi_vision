from uuid import uuid4

from fastapi import HTTPException, UploadFile
from fastapi.responses import Response
from starlette import concurrency, status

from src.core.exception import NotImageError
from src.db.entity.enum import ocr_enum
from src.dependency.ports import ImageRepository, OcrMetaRepository
from src.domain.user.model import user_request

from ..converter import image_converter
from ..model import ocr_model, ocr_request, ocr_response
from ..service import image_logic


async def upload_image(
    *,
    user: user_request.UserCurrent,
    meta_repo: OcrMetaRepository,
    image_repo: ImageRepository,
    file: UploadFile,
) -> None:
    file_name = file.filename if file.filename else uuid4().hex
    if len(file_name) > ocr_enum.ImageEntityEnum.NAME:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="file name too long",
        )
    if not file.content_type or file.content_type.split("/")[0] != "image":
        raise NotImageError
    media_type = file.content_type
    image = await file.read()

    thumb_io = await concurrency.run_in_threadpool(image_logic.create_thumb, data=image)
    thumb_id = await image_logic.save_thumb(
        image_repo=image_repo,
        thumbnail=await thumb_io,
    )

    image_id = await image_logic.save_image(
        image_repo=image_repo,
        image=image,
        file_name=file_name,
    )

    await image_logic.save_image_metadata(
        current_user=user,
        repo=meta_repo,
        file_name=file_name,
        media_type=media_type,
        image_id=image_id,
        thumbnail_id=thumb_id,
    )


async def get_image_list(
    *,
    repo: OcrMetaRepository,
    keyword: str | None,
    size: int,
    page: int,
) -> list[ocr_response.ImageResponse]:
    entity_list = await image_logic.get_image_list(
        repo=repo,
        keyword=keyword,
        size=size,
        page=page,
    )
    res = [await image_converter.to_image_response(v) for v in entity_list]
    return res


async def get_image(
    *,
    meta_repo: OcrMetaRepository,
    image_repo: ImageRepository,
    image_id: int,
) -> Response:
    image_entity = await image_logic.get_image_meta(repo=meta_repo, image_id=image_id)
    image_data = await image_logic.get_image(repo=image_repo, metadata=image_entity)
    return Response(
        content=image_data,
        media_type=image_entity.media_type,
    )


async def get_thumbnail(
    *,
    meta_repo: OcrMetaRepository,
    image_repo: ImageRepository,
    image_id: int,
) -> Response:
    image_entity = await image_logic.get_image_meta(repo=meta_repo, image_id=image_id)
    image_document = await image_logic.get_thumbnail(
        repo=image_repo, metadata=image_entity
    )
    image_data = ocr_model.ThumbnailMongoModel.model_validate(obj=image_document)
    return Response(
        content=image_data.file,
        media_type=image_entity.media_type,
    )


async def update_image(
    *,
    user: user_request.UserCurrent,
    meta_repo: OcrMetaRepository,
    image_repo: ImageRepository,
    image_id: int,
    data: ocr_request.ImageUpdateRequest,
):
    image_entity = await image_logic.get_image_meta(repo=meta_repo, image_id=image_id)
    await image_logic.verify_author(current_user=user, metadata=image_entity)
    await image_logic.update_image_data(
        repo=image_repo,
        metadata=image_entity,
        data=data,
    )
    await image_logic.update_image_meta(
        repo=meta_repo,
        metadata=image_entity,
        data=data,
    )


async def delete_image(
    *,
    user: user_request.UserCurrent,
    meta_repo: OcrMetaRepository,
    image_repo: ImageRepository,
    image_id: int,
) -> None:
    image_entity = await image_logic.get_image_meta(repo=meta_repo, image_id=image_id)
    await image_logic.verify_author(current_user=user, metadata=image_entity)
    await image_logic.delete_thumbnail(repo=image_repo, metadata=image_entity)
    await image_logic.delete_image(repo=image_repo, metadata=image_entity)
    await image_logic.delete_image_meta(repo=meta_repo, image_id=image_id)
