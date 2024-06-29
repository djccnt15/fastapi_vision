from datetime import datetime
from typing import Iterable, Sequence, Tuple

from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete, func, insert, or_, select, update

from src.db.entity.ocr_entity import ImageEntity, OcrEntity
from src.db.entity.user_entity import UserEntity
from src.dependency.ports import OcrMetaRepository


class RdbOcrRepository(OcrMetaRepository):
    def __init__(self, *, db: AsyncSession):
        self.db = db

    async def create_image_meta(
        self,
        *,
        file_name: str,
        media_type: str,
        image_id: str,
        thumbnail_id: str,
        created_datetime: datetime,
        user_id: int,
    ) -> None:
        q = insert(ImageEntity).values(
            name=file_name,
            media_type=media_type,
            image_id=image_id,
            thumbnail_id=thumbnail_id,
            created_datetime=created_datetime,
            user_id=user_id,
        )
        await self.db.execute(statement=q)
        await self.db.commit()

    async def create_ocr_result_meta(
        self,
        *,
        version: int,
        created_datetime: datetime,
        image_id: int,
        user_id: int,
        content_ids: Iterable[str],
    ) -> None:
        data = [
            {
                "version": version,
                "created_datetime": created_datetime,
                "image_id": image_id,
                "user_id": user_id,
                "content_id": content_id,
            }
            for content_id in content_ids
        ]
        q = insert(OcrEntity).values(data)
        await self.db.execute(statement=q)
        await self.db.commit()

    async def read_image_list(
        self,
        *,
        keyword: str | None,
        size: int,
        page: int,
    ) -> Sequence[Row[Tuple[ImageEntity, UserEntity]]]:
        q = select(ImageEntity, UserEntity).join(
            target=UserEntity,
            onclause=ImageEntity.user_id == UserEntity.id,
        )

        if keyword:
            keyword = f"%{keyword}%"
            q = q.where(
                or_(
                    ImageEntity.name.ilike(keyword),
                    UserEntity.name.ilike(keyword),
                )
            )

        q = q.order_by(ImageEntity.id.desc()).offset(page).limit(size)
        res = await self.db.execute(statement=q)
        return res.all()

    async def read_image_meta(self, *, image_id: int) -> ImageEntity | None:
        q = select(ImageEntity).where(ImageEntity.id == image_id)
        res = await self.db.execute(statement=q)
        return res.scalar()

    async def read_ocr_last_version(self, *, image_id: int) -> int | None:
        q = (
            select(func.max(OcrEntity.version))
            .where(OcrEntity.image_id == image_id)
            .group_by(OcrEntity.image_id)
        )
        res = await self.db.execute(statement=q)
        return res.scalar()

    async def read_ocr_result_meta(
        self,
        *,
        image_id: int,
        version: int | None,
    ) -> Sequence[OcrEntity]:
        q = select(OcrEntity).where(OcrEntity.image_id == image_id)
        if version:
            q = q.where(OcrEntity.version == version)
        q = q.order_by(OcrEntity.id.desc())

        res = await self.db.execute(statement=q)
        return res.scalars().all()

    async def read_result_by_content_id(self, *, content_id: str) -> OcrEntity | None:
        q = select(OcrEntity).where(OcrEntity.content_id == content_id)
        res = await self.db.execute(statement=q)
        return res.scalar()

    async def update_image_meta(
        self,
        *,
        image_id: int,
        name: str,
    ) -> None:
        q = update(ImageEntity).where(ImageEntity.id == image_id).values(name=name)
        await self.db.execute(statement=q)
        await self.db.commit()

    async def delete_image_meta(self, *, image_id: int) -> None:
        q = delete(ImageEntity).where(ImageEntity.id == image_id)
        await self.db.execute(statement=q)
        await self.db.commit()

    async def delete_ocr_meta(self, *, content_id: str) -> None:
        q = delete(OcrEntity).where(OcrEntity.content_id == content_id)
        await self.db.execute(statement=q)
        await self.db.commit()
