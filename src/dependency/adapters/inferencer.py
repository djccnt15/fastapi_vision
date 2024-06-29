from pathlib import Path

import pytesseract
from PIL import Image
from starlette import concurrency

from src.core.utils import crop_image
from src.dependency.ports import OcrInferencer
from src.domain.ocr.model import ocr_model


class TesseractInferencer(OcrInferencer):
    _instance = None

    def __new__(cls, path: Path, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TesseractInferencer, cls).__new__(
                cls, *args, **kwargs
            )
            pytesseract.pytesseract.tesseract_cmd = path
        return cls._instance

    async def extract_text(
        self,
        *,
        image: Image.Image,
        roi: ocr_model.Roi,
        lang: str | None = None,
        config: str = "",
        nice: int = 0,
        timeout: int = 0,
    ) -> list[str]:
        image = crop_image(image=image, roi=roi)
        extracted_text: str = await concurrency.run_in_threadpool(
            func=pytesseract.image_to_string,
            image=image,
            lang=lang,
            config=config,
            nice=nice,
            timeout=timeout,
        )
        res = extracted_text.replace("\n", "").split(" ")
        return res
