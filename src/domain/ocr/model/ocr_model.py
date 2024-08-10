from datetime import datetime
from typing import NamedTuple, Self

from fastapi import HTTPException
from pydantic import BaseModel, Field, model_validator
from starlette import status


class ThumbnailMongoModel(BaseModel):
    file: bytes


class OcrResultMeta(NamedTuple):
    version: int
    created_datetime: datetime


class Roi(BaseModel):
    x1: int = Field(ge=0)
    y1: int = Field(ge=0)
    x2: int = Field(ge=0)
    y2: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_roi(self) -> Self:
        conditions = [
            self.x1 > self.x2,
            self.y1 > self.y2,
        ]
        if any(conditions):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="roi validation error",
            )
        return self


class OcrResultBase(BaseModel):
    roi: Roi
    detail: list[str]
