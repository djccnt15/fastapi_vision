from datetime import datetime
from io import BytesIO
from typing import Any, Sequence, Tuple

from PIL import Image, UnidentifiedImageError
from sqlalchemy.engine.row import Row

from src.core import configs
from src.core.exception import InvalidUserError, NotImageError, QueryResultEmptyError
from src.db.entity.ocr_entity import ImageEntity
from src.db.entity.user_entity import UserEntity
from src.dependency import ports
from src.domain.user.model import user_request

from ..model import ocr_model, ocr_request

config = configs.config.ocr


async def create_thumb(*, data: bytes) -> BytesIO:
    try:
        image = Image.open(BytesIO(data))
    except UnidentifiedImageError:
        raise NotImageError

    thumbnail = image.copy()
    thumbnail.thumbnail(size=(config.thumbnail.width, config.thumbnail.height))

    thumb_io = BytesIO()
    thumbnail.save(thumb_io, format=image.format)
    thumb_io.seek(0)
    return thumb_io


async def save_thumb(
    *,
    image_repo: ports.ImageRepository,
    thumbnail: BytesIO,
) -> str:
    document = ocr_model.ThumbnailMongoModel(file=thumbnail.read())
    inserted_id = await image_repo.upload_thumbnail(data=document.model_dump())
    return inserted_id


async def save_image(
    *,
    image_repo: ports.ImageRepository,
    image: bytes,
    file_name: str,
) -> str:
    res = await image_repo.upload_image(
        file_name=file_name,
        file=image,
    )
    return res


async def save_image_metadata(
    *,
    current_user: user_request.UserCurrent,
    repo: ports.OcrMetaRepository,
    file_name: str,
    media_type: str,
    image_id: str,
    thumbnail_id: str,
) -> None:
    await repo.create_image_meta(
        file_name=file_name,
        media_type=media_type,
        image_id=image_id,
        thumbnail_id=thumbnail_id,
        created_datetime=datetime.now(configs.KST),
        user_id=current_user.id,
    )


async def get_image_list(
    *,
    repo: ports.OcrMetaRepository,
    keyword: str | None,
    size: int,
    page: int,
) -> Sequence[Row[Tuple[ImageEntity, UserEntity]]]:
    entity_list = await repo.read_image_list(keyword=keyword, size=size, page=page)
    return entity_list


async def get_image_meta(
    *,
    repo: ports.OcrMetaRepository,
    image_id: int,
) -> ImageEntity:
    image_entity = await repo.read_image_meta(image_id=image_id)
    if not image_entity:
        raise QueryResultEmptyError
    return image_entity


async def get_image(
    *,
    repo: ports.ImageRepository,
    metadata: ImageEntity,
) -> Any:
    image = await repo.download_image(file_id=metadata.image_id)
    return image


async def get_thumbnail(
    *,
    repo: ports.ImageRepository,
    metadata: ImageEntity,
) -> Any:
    image = await repo.download_thumbnail(thumbnail_id=metadata.thumbnail_id)
    if not image:
        raise QueryResultEmptyError
    return image


async def verify_author(
    *,
    current_user: user_request.UserCurrent,
    metadata: ImageEntity,
) -> None:
    if metadata.user_id != current_user.id:
        raise InvalidUserError


async def update_image_meta(
    *,
    repo: ports.OcrMetaRepository,
    metadata: ImageEntity,
    data: ocr_request.ImageUpdateRequest,
) -> None:
    await repo.update_image_meta(image_id=metadata.id, name=data.name)


async def update_image_data(
    *,
    repo: ports.ImageRepository,
    metadata: ImageEntity,
    data: ocr_request.ImageUpdateRequest,
) -> None:
    await repo.update_image(image_id=metadata.image_id, name=data.name)


async def delete_thumbnail(
    *,
    repo: ports.ImageRepository,
    metadata: ImageEntity,
) -> None:
    await repo.delete_thumbnail(thumbnail_id=metadata.thumbnail_id)


async def delete_image(
    *,
    repo: ports.ImageRepository,
    metadata: ImageEntity,
) -> None:
    await repo.delete_image(image_id=metadata.image_id)


async def delete_image_meta(
    *,
    repo: ports.OcrMetaRepository,
    image_id: int,
) -> None:
    await repo.delete_image_meta(image_id=image_id)
