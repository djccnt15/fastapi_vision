from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert

from src.db.entity.vision_entity import DeftDetailEntity, ResultEntity
from src.dependency.ports.vision import VisionRepository


class RdbVisionRepository(VisionRepository):
    def __init__(self, *, db: AsyncSession):
        self.db = db

    async def create_result(
        self,
        *,
        serial_num: str,
        spec: dict,
        created_datetime: datetime,
        prod_type_id: int,
        result_type: int,
    ) -> None:
        q = insert(ResultEntity).values(
            serial_num=serial_num,
            spec=spec,
            created_datetime=created_datetime,
            prod_type_id=prod_type_id,
            result_type_id=result_type,
        )
        await self.db.execute(statement=q)
        await self.db.commit()

    async def create_deft_detail(
        self,
        *,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        detail: dict,
        result_id: int,
        deft_type_id: int,
    ) -> None:
        q = insert(DeftDetailEntity).values(
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
            detail=detail,
            result_id=result_id,
            deft_type_id=deft_type_id,
        )
        await self.db.execute(statement=q)
        await self.db.commit()
