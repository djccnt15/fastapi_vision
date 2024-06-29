from abc import ABC, abstractmethod
from typing import Any


class ImageRepository(ABC):

    @abstractmethod
    async def upload_image(
        self,
        *,
        chunk_size: int = 1024,
        file_name: str,
        file: bytes,
    ) -> str: ...

    @abstractmethod
    async def upload_thumbnail(self, *, data: dict) -> str: ...

    @abstractmethod
    async def download_image(self, *, file_id: str) -> Any: ...

    @abstractmethod
    async def download_thumbnail(self, *, thumbnail_id: str) -> Any | None: ...

    @abstractmethod
    async def update_image(
        self,
        *,
        image_id: str,
        name: str,
    ) -> None: ...

    @abstractmethod
    async def delete_image(self, *, image_id: str) -> None: ...

    @abstractmethod
    async def delete_thumbnail(self, *, thumbnail_id: str) -> None: ...
