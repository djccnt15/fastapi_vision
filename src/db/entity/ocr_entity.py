from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import BigInteger, DateTime, Integer, String

from . import BigintIdEntity
from .enum.ocr_enum import ImageEntityEnum
from .user_entity import UserEntity


class ImageEntity(BigintIdEntity):
    __tablename__ = "image"

    name: Mapped[str] = mapped_column(String(length=ImageEntityEnum.NAME.value))
    media_type: Mapped[str] = mapped_column(String(length=ImageEntityEnum.TYPE.value))
    image_id: Mapped[str] = mapped_column(
        String(length=ImageEntityEnum.OBJECT_ID.value),
        doc="original image id at MongoDB",
    )
    thumbnail_id: Mapped[str] = mapped_column(
        String(length=ImageEntityEnum.OBJECT_ID.value),
        doc="thumbnail image id at MongoDB",
    )
    created_datetime: Mapped[datetime] = mapped_column(DateTime)
    user_id: Mapped["UserEntity"] = mapped_column(BigInteger, ForeignKey(UserEntity.id))


class OcrEntity(BigintIdEntity):
    __tablename__ = "ocr"

    version: Mapped[int] = mapped_column(Integer, default=1)
    created_datetime: Mapped[datetime] = mapped_column(DateTime)
    image_id: Mapped["ImageEntity"] = mapped_column(
        BigInteger,
        ForeignKey(ImageEntity.id),
    )
    user_id: Mapped["UserEntity"] = mapped_column(BigInteger, ForeignKey(UserEntity.id))
    content_id: Mapped[str] = mapped_column(
        String(length=ImageEntityEnum.OBJECT_ID.value),
        unique=True,
    )
