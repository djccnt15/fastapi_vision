from typing import Any

from ..model import ocr_response


async def to_OcrResult(*, ocr_result: dict[str, Any]) -> ocr_response.OcrResult:
    return ocr_response.OcrResult(
        id=str(ocr_result.get("_id", None)),
        roi=ocr_result.get("roi", None),
        detail=ocr_result.get("detail", None),
    )
