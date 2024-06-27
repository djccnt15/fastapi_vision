from datetime import datetime
from typing import Union

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import BigInteger, DateTime, String

from . import BaseEntity, BigintIdEntity
from .enum.user_enum import (
    RoleEntityEnum,
    StateEntityEnum,
    UserEntityEnum,
    UserStateEntityEnum,
)


class RoleEntity(BigintIdEntity):
    __tablename__ = "role"

    name: Mapped[str] = mapped_column(
        String(length=RoleEntityEnum.NAME.value),
        unique=True,
    )


class UserEntity(BigintIdEntity):
    __tablename__ = "user"

    name: Mapped[str | None] = mapped_column(
        String(length=UserEntityEnum.NAME.value),
        unique=True,
        index=True,
    )
    password: Mapped[str | None] = mapped_column(
        String(length=UserEntityEnum.PASSWORDMAX.value),
    )
    email: Mapped[str | None] = mapped_column(
        String(length=UserEntityEnum.EMAIL.value),
        unique=True,
        index=True,
    )
    created_datetime: Mapped[datetime] = mapped_column(DateTime)
    role_id: Mapped[Union["RoleEntity", None]] = mapped_column(
        BigInteger,
        ForeignKey(RoleEntity.id),
    )

    state = relationship(
        argument="StateEntity",
        secondary="user_state",
        back_populates="user",
        lazy="selectin",
    )


class StateEntity(BigintIdEntity):
    __tablename__ = "state"

    name: Mapped[str] = mapped_column(
        String(length=StateEntityEnum.NAME.value),
        unique=True,
    )

    user = relationship(
        argument="UserEntity",
        secondary="user_state",
        back_populates="state",
        lazy="selectin",
    )


class UserStateEntity(BaseEntity):
    __tablename__ = "user_state"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(UserEntity.id),
        primary_key=True,
    )
    state_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(StateEntity.id),
        primary_key=True,
    )
    detail: Mapped[str | None] = mapped_column(
        String(length=UserStateEntityEnum.DETAIL.value)
    )
    created_datetime: Mapped[datetime] = mapped_column(DateTime)


class LoggedInEntity(BigintIdEntity):
    __tablename__ = "logged_in"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(UserEntity.id))
    created_datetime: Mapped[datetime] = mapped_column(DateTime)
