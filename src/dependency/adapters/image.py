from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorGridFSBucket

from src.dependency.ports import ImageRepository


class MongoImageRepository(ImageRepository):

    def __init__(self, *, db: AsyncIOMotorDatabase) -> None:
        self.bucket = AsyncIOMotorGridFSBucket(database=db)
        self.thumbnail_collection = db.get_collection(name="thumbnail")

    async def upload_image(
        self,
        *,
        chunk_size: int = 1024,
        file_name: str,
        file: bytes,
    ) -> str:
        file_id = await self.bucket.upload_from_stream(
            filename=file_name,
            source=file,
            chunk_size_bytes=chunk_size,
        )
        return str(file_id)

    async def upload_thumbnail(self, *, data: dict) -> str:
        inserted_id = await self.thumbnail_collection.insert_one(document=data)
        return inserted_id.inserted_id

    async def download_image(self, *, file_id: str) -> Any:
        grid_out = await self.bucket.open_download_stream(file_id=ObjectId(file_id))
        contents = await grid_out.read()
        return contents

    async def download_thumbnail(self, *, thumbnail_id: str) -> Any | None:
        thumbnail = await self.thumbnail_collection.find_one(
            filter={"_id": ObjectId(thumbnail_id)}
        )
        return thumbnail

    async def update_image(self, *, image_id: str, name: str) -> None:
        await self.bucket.rename(file_id=ObjectId(image_id), new_filename=name)

    async def delete_image(self, *, image_id: str) -> None:
        await self.bucket.delete(file_id=ObjectId(image_id))

    async def delete_thumbnail(self, *, thumbnail_id: str) -> None:
        await self.thumbnail_collection.delete_one(
            filter={"_id": ObjectId(thumbnail_id)}
        )
