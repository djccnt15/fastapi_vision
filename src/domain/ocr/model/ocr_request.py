from pydantic import BaseModel


class ImageUpdateRequest(BaseModel):
    name: str
