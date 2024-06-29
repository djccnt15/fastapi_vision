from abc import ABC, abstractmethod

from PIL import Image

from src.domain.ocr.model import ocr_model


class OcrInferencer(ABC):

    @abstractmethod
    async def extract_text(
        self,
        *,
        image: Image.Image,
        roi: ocr_model.Roi,
        lang: str | None = None,
        config: str = "",
        nice: int = 0,
        timeout: int = 0,
    ) -> list[str]: ...
