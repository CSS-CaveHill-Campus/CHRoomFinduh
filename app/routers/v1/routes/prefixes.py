from fastapi import APIRouter, Depends, Request
from typing import Annotated

from app.db.mongo_client import MongoORM
from app.schemas.params import PrefixesParams
from app.schemas import PrefixSuccessResponse
from app.schemas.failure_response import FailureResponse
from app.models.prefix import Prefix

prefixes_router = APIRouter(prefix="/prefixes")


@prefixes_router.get("/", response_model=PrefixSuccessResponse, responses={404: {"model": FailureResponse}})
async def get_prefixes(
    request: Request,
    params: Annotated[PrefixesParams, Depends()],
) -> PrefixSuccessResponse:
    db: MongoORM = request.app.state.db
    prefixes = await db.get_prefix_details(faculty=params.faculty)
    return PrefixSuccessResponse(data=prefixes)
