from datetime import datetime
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert, select

from src.db.entity.vision_entity import (
    DeftDetailEntity,
    DeftTypeEntity,
    DetectorEntity,
    ProdDeftEntity,
    ProdTypeEntity,
    ResultEntity,
    ResultTypeEntity,
    RoiEntity,
)
from src.dependency.ports.vision import VisionRepository


class RdbVisionRepository(VisionRepository):
    def __init__(self, *, db: AsyncSession):
        self.db = db

    async def read_prod_type(self) -> Sequence[ProdTypeEntity]:
        q = select(ProdTypeEntity)
        res = await self.db.execute(statement=q)
        return res.scalars().all()

    async def read_deft_type(self) -> Sequence[DeftTypeEntity]:
        q = select(DeftTypeEntity)
        res = await self.db.execute(statement=q)
        return res.scalars().all()

    async def read_detector(self) -> Sequence[DetectorEntity]:
        q = select(DetectorEntity)
        res = await self.db.execute(statement=q)
        return res.scalars().all()

    async def read_result_type(self) -> Sequence[ResultTypeEntity]:
        q = select(ResultTypeEntity)
        res = await self.db.execute(statement=q)
        return res.scalars().all()

    async def read_prod_deft(self) -> Sequence[ProdDeftEntity]:
        q = select(ProdDeftEntity)
        res = await self.db.execute(statement=q)
        return res.scalars().all()

    async def read_roi(self) -> Sequence[RoiEntity]:
        q = select(RoiEntity)
        res = await self.db.execute(statement=q)
        return res.scalars().all()

    async def create_result(
        self,
        *,
        serial_num: str,
        spec: dict,
        created_datetime: datetime,
        prod_type_id: int,
        side_id: int,
        result_type_id: int,
    ) -> None:
        q = insert(ResultEntity).values(
            serial_num=serial_num,
            spec=spec,
            created_datetime=created_datetime,
            prod_type_id=prod_type_id,
            side_id=side_id,
            result_type_id=result_type_id,
        )
        await self.db.execute(statement=q)
        await self.db.commit()

    async def create_deft_detail(
        self,
        *,
        detail: dict,
        result_id: int,
        roi_id: int,
    ) -> None:
        q = insert(DeftDetailEntity).values(
            detail=detail,
            result_id=result_id,
            roi_id=roi_id,
        )
        await self.db.execute(statement=q)
        await self.db.commit()
