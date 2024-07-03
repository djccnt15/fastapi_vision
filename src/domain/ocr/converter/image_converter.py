from typing import Tuple

from sqlalchemy.engine.row import Row

from src.db.entity.ocr_entity import ImageEntity
from src.db.entity.user_entity import UserEntity

from ..model import ocr_response


async def to_image_response(
    data: Row[Tuple[ImageEntity, UserEntity]]
) -> ocr_response.ImageResponse:
    image_entity: ImageEntity = data[0]
    user_entity: UserEntity = data[1]

    res = ocr_response.ImageResponse(
        id=image_entity.id,
        name=image_entity.name,
        created_datetime=image_entity.created_datetime,
        user=user_entity.name,
    )
    return res
