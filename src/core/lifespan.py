from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.dependency import adapters


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # Check DB availability
    await adapters.db_ping()
    await adapters.blob_ping()

    yield

    # close DB engine
    await adapters.db_engine.dispose()
    adapters.mongodb_client.close()
