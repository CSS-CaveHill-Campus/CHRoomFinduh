from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.routers import v1_router
from dotenv import load_dotenv
from os import getenv

from app.db.mongo_client import MongoORM

success: bool = load_dotenv()

if not success:
    raise RuntimeError("Can not load env file")


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo_url: str | None = getenv("MONGO_URL")
    if not mongo_url:
        raise RuntimeError("Mongo URL not set")

    app.state.db = MongoORM(mongo_url)

    yield

    app.state.db.close()


app = FastAPI(title="UWI FindYuhRoom API", lifespan=lifespan)


app.include_router(router=v1_router)


@app.get("/")
async def index():
    return "Hello world!"
