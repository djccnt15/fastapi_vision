from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable, Sequence, Tuple

from sqlalchemy.engine.row import Row

from src.db.entity.ocr_entity import ImageEntity, OcrEntity
from src.db.entity.user_entity import UserEntity


class OcrMetaRepository(ABC):

    @abstractmethod
    async def create_image_meta(
        self,
        *,
        file_name: str,
        media_type: str,
        image_id: str,
        thumbnail_id: str,
        created_datetime: datetime,
        user_id: int,
    ) -> None: ...

    @abstractmethod
    async def create_ocr_result_meta(
        self,
        *,
        version: int,
        created_datetime: datetime,
        image_id: int,
        user_id: int,
        content_ids: Iterable[str],
    ) -> None: ...

    @abstractmethod
    async def read_image_list(
        self,
        *,
        keyword: str | None,
        size: int,
        page: int,
    ) -> Sequence[Row[Tuple[ImageEntity, UserEntity]]]: ...

    @abstractmethod
    async def read_image_meta(self, *, image_id: int) -> ImageEntity | None: ...

    @abstractmethod
    async def read_ocr_last_version(self, *, image_id: int) -> int | None: ...

    @abstractmethod
    async def read_ocr_result_meta(
        self,
        *,
        image_id: int,
        version: int | None,
    ) -> Sequence[OcrEntity]: ...

    @abstractmethod
    async def read_result_by_content_id(
        self, *, content_id: str
    ) -> OcrEntity | None: ...

    @abstractmethod
    async def update_image_meta(
        self,
        *,
        image_id: int,
        name: str,
    ) -> None: ...

    @abstractmethod
    async def delete_image_meta(self, *, image_id: int) -> None: ...

    @abstractmethod
    async def delete_ocr_meta(self, *, content_id: str) -> None: ...
