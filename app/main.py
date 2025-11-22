from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers import v1_router
from dotenv import load_dotenv
from os import getenv

from app.db.mongo_client import MongoORM

success: bool = load_dotenv()

if not success:
    print("Can not load env file")


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo_url: str | None = getenv("MONGO_URL")
    db_name: str | None = getenv("DB_NAME")
    if not mongo_url or not db_name:
        raise RuntimeError("Mongo URL or DB name not set")

    app.state.db = MongoORM(mongo_url, db_name)

    yield

    app.state.db.close()


app = FastAPI(title="UWI CH RoomFinduh API", lifespan=lifespan)
templates = Jinja2Templates(directory="app/templates")


app.include_router(router=v1_router)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
