from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.sql import select

from src.core import configs

from .image import MongoImageRepository
from .inferencer import TesseractInferencer
from .ocr import MongoOcrRepository
from .ocr_meta import RdbOcrRepository
from .user import RdbUserRepository

config = configs.config

DB_URL = URL.create(**config.db.url)
db_engine = create_async_engine(
    url=DB_URL,
    **config.db.engine,
)


async def db_ping():
    db = AsyncSession(bind=db_engine)
    q = select(1)
    try:
        res = await db.execute(statement=q)
    finally:
        await db.close()
    return res.scalar()


async def get_db():
    db = AsyncSession(bind=db_engine)
    try:
        yield db
    finally:
        await db.close()


RepoSession = Annotated[AsyncSession, Depends(get_db)]


async def get_user_repo(db: RepoSession) -> RdbUserRepository:
    return RdbUserRepository(db=db)


async def get_ocr_meta_repo(db: RepoSession) -> RdbOcrRepository:
    return RdbOcrRepository(db=db)


tesseract = TesseractInferencer(path=config.ocr.tesseract_path)


async def get_ocr_inferencer() -> TesseractInferencer:
    return tesseract


mongodb_client = AsyncIOMotorClient(config.mongodb.uri)


async def blob_ping():
    db: AsyncIOMotorDatabase = mongodb_client.get_database(**config.mongodb.db)
    return await db.command("ping")


async def get_blob_db():
    db: AsyncIOMotorDatabase = mongodb_client.get_database(**config.mongodb.db)
    try:
        yield db
    finally:
        ...


BlobClient = Annotated[AsyncIOMotorDatabase, Depends(get_blob_db)]


async def get_image_repo(db: BlobClient) -> MongoImageRepository:
    return MongoImageRepository(db=db)


async def get_ocr_repo(db: BlobClient) -> MongoOcrRepository:
    return MongoOcrRepository(db=db)
