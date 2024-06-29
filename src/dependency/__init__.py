from typing import Annotated

from fastapi import Depends

from . import adapters, ports

UserRepo = Annotated[ports.UserRepository, Depends(adapters.get_user_repo)]
MetaRepo = Annotated[ports.OcrMetaRepository, Depends(adapters.get_ocr_meta_repo)]
ImageRepo = Annotated[ports.ImageRepository, Depends(adapters.get_image_repo)]
OcrRepo = Annotated[ports.OcrRepository, Depends(adapters.get_ocr_repo)]
