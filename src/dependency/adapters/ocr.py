from typing import Any, Iterable

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.core.exception import QueryResultEmptyError
from src.dependency.ports import OcrRepository
from src.domain.ocr.model import ocr_model


class MongoOcrRepository(OcrRepository):

    def __init__(self, *, db: AsyncIOMotorDatabase) -> None:
        self.collection = db.get_collection(name="ocr_res")

    async def create_ocr_result(self, *, doc: list[dict[str, Any]]) -> Iterable[str]:
        res = await self.collection.insert_many(documents=doc)
        return (str(v) for v in res.inserted_ids)

    async def read_result_by_content_id(self, *, content_id: str) -> dict[str, Any]:
        ocr_result: dict[str, Any] | None = await self.collection.find_one(
            filter={"_id": ObjectId(content_id)}
        )  # type: ignore
        if not ocr_result:
            raise QueryResultEmptyError
        return ocr_result

    async def update_ocr_result(
        self,
        *,
        content_id: str,
        data: ocr_model.OcrResultBase,
    ) -> None:
        await self.collection.update_one(
            filter={"_id": ObjectId(content_id)},
            update={"$set": data.model_dump()},
        )

    async def delete_ocr_result(self, *, content_id: str) -> None:
        await self.collection.delete_one(filter={"_id": ObjectId(content_id)})
