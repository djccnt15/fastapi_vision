from abc import ABC, abstractmethod
from datetime import datetime
from typing import Sequence

from src.db.entity.vision_entity import (
    DeftTypeEntity,
    DetectorEntity,
    ProdDeftEntity,
    ProdTypeEntity,
    ResultTypeEntity,
    RoiEntity,
)


class VisionRepository(ABC):

    @abstractmethod
    async def read_prod_type(self) -> Sequence[ProdTypeEntity]: ...

    @abstractmethod
    async def read_deft_type(self) -> Sequence[DeftTypeEntity]: ...

    @abstractmethod
    async def read_detector(self) -> Sequence[DetectorEntity]: ...

    @abstractmethod
    async def read_result_type(self) -> Sequence[ResultTypeEntity]: ...

    @abstractmethod
    async def read_prod_deft(self) -> Sequence[ProdDeftEntity]: ...

    @abstractmethod
    async def read_roi(self) -> Sequence[RoiEntity]: ...

    @abstractmethod
    async def create_result(
        self,
        *,
        serial_num: str,
        spec: dict,
        created_datetime: datetime,
        prod_type_id: int,
        side_id: int,
        result_type_id: int,
    ) -> None: ...

    @abstractmethod
    async def create_deft_detail(
        self,
        *,
        detail: dict,
        result_id: int,
        roi_id: int,
    ) -> None: ...
