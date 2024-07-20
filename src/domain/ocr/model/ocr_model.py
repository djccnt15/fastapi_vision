from datetime import datetime
from typing import NamedTuple, Self

from fastapi import HTTPException
from pydantic import BaseModel, model_validator
from starlette import status


class ThumbnailMongoModel(BaseModel):
    file: bytes


class OcrResultMeta(NamedTuple):
    version: int
    created_datetime: datetime


class Roi(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int

    @model_validator(mode="after")
    def validate_roi(self) -> Self:
        conditions = [
            min(self.x1, self.y1, self.x2, self.y2) < 0,
            self.x1 > self.x2,
            self.y1 > self.y2,
        ]
        if any(conditions):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="roi error",
            )
        return self


class OcrResultBase(BaseModel):
    roi: Roi
    detail: list[str]
