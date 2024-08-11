from abc import ABC, abstractmethod
from datetime import datetime


class VisionRepository(ABC):

    @abstractmethod
    async def create_result(
        self,
        *,
        serial_num: str,
        spec: dict,
        created_datetime: datetime,
        prod_type_id: int,
        result_type: int,
    ) -> None: ...

    @abstractmethod
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
    ) -> None: ...
