from abc import ABC, abstractmethod
from typing import Any, Iterable

from src.domain.ocr.model import ocr_model


class OcrRepository(ABC):

    @abstractmethod
    async def create_ocr_result(
        self, *, doc: list[dict[str, Any]]
    ) -> Iterable[str]: ...

    @abstractmethod
    async def read_result_by_content_id(self, *, content_id: str) -> dict[str, Any]: ...

    @abstractmethod
    async def update_ocr_result(
        self,
        *,
        content_id: str,
        data: ocr_model.OcrResultBase,
    ) -> None: ...

    @abstractmethod
    async def delete_ocr_result(self, *, content_id: str) -> None: ...
