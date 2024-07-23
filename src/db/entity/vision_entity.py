from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import JSON, BigInteger, Boolean, DateTime, Integer, String

from . import BigintIdEntity
from .enum.vision_enum import (
    DeftTypeEntityEnum,
    ProdTypeEntityEnum,
    ResultEntityEnum,
    ResultTypeEntityEnum,
)


class ProdTypeEntity(BigintIdEntity):
    __tablename__ = "prod_type"

    name: Mapped[str] = mapped_column(String(length=ProdTypeEntityEnum.NAME.value))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class DeftTypeEntity(BigintIdEntity):
    __tablename__ = "deft_type"

    name: Mapped[str] = mapped_column(String(length=DeftTypeEntityEnum.NAME.value))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class ProdDeftEntity(BigintIdEntity):
    __tablename__ = "prod_deft"

    prod_type_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(ProdTypeEntity.id))
    deft_type_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(DeftTypeEntity.id))


class RoiEntity(BigintIdEntity):
    __tablename__ = "roi"

    x1: Mapped[int] = mapped_column(Integer)
    y1: Mapped[int] = mapped_column(Integer)
    x2: Mapped[int] = mapped_column(Integer)
    y2: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    prod_deft_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(ProdDeftEntity.id))


class ResultTypeEntity(BigintIdEntity):
    __tablename__ = "result_type"

    name: Mapped[str] = mapped_column(
        String(length=ResultTypeEntityEnum.NAME.value),
        unique=True,
    )


class ResultEntity(BigintIdEntity):
    __tablename__ = "result"

    serial_num: Mapped[str] = mapped_column(
        String(length=ResultEntityEnum.SERIAL_NUM.value)
    )
    spec: Mapped[dict] = mapped_column(JSON)
    created_datetime: Mapped[datetime] = mapped_column(DateTime)
    result_type_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(ResultTypeEntity.id),
    )


class DeftHistoryEntity(BigintIdEntity):
    __tablename__ = "deft_history"

    result_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(ResultEntity.id))
    roi_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(RoiEntity.id))
