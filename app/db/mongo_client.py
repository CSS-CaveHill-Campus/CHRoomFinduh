"""This class will control the Mongo DB interaction"""

import json
from typing import cast
import aiofiles
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)

from app.schemas.enums import DayEnum, FacultyEnum
from app.models import Schedule
from app.models.room import Room


class MongoORM:
    client: AsyncIOMotorClient[dict[str, object]]

    db: AsyncIOMotorDatabase[dict[str, object]]
    db_name: str

    schedule_collection_name: str = "schedule"

    schedule_collection: AsyncIOMotorCollection[dict[str, object]]
    rooms_collection: AsyncIOMotorCollection[dict[str, object]]
    room_availabilities_collection: AsyncIOMotorCollection[dict[str, object]]
    course_prefixes_collection: AsyncIOMotorCollection[dict[str, object]]

    def __init__(self, url: str, db_name: str):
        self.client = AsyncIOMotorClient(url)
        self.db_name = db_name

        self.db = self.client.get_database(self.db_name)

        self.schedule_collection = self.db[self.schedule_collection_name]
        self.rooms_collection = self.db["rooms"]
        self.room_availabilities_collection = self.db["room_availabilities"]
        self.course_prefixes_collection = self.db["course_prefixes"]

    async def get_schedules(
        self,
        faculty: FacultyEnum | None = None,
        limit: int = 20,
        day: DayEnum | None = None,
        room: str | None = None,
        prefix: str | None = None,
    ) -> list[Schedule]:
        query = {}
        if day:
            query["day"] = day.value
        if room:
            query["room"] = room

        if faculty and not prefix:
            faculty_prefixes = await self.get_prefixes(faculty=faculty)
            query["course_code"] = {
                "$regex": f"^({'|'.join(faculty_prefixes)})"
            }
        if prefix:  # Prefix takes precedence
            query["course_code"] = {"$regex": f"^{prefix}"}

        cursor = self.schedule_collection.find(query, {"_id": 0})
        if limit > 0:
            cursor = cursor.limit(limit)

        return cast(
            list[Schedule], await cursor.to_list(length=limit if limit > 0 else None)
        )

    async def get_rooms(self):
        async with aiofiles.open("app/public/rooms.json", mode="r") as f:
            content = await f.read()
        rooms: list[Room] = cast(list[Room], json.loads(content))
        return rooms

    async def get_prefixes(self, faculty: FacultyEnum | None = None):
        async with aiofiles.open("app/public/prefixes.json", mode="r") as f:
            content = await f.read()
        data: list[dict[str, str]] = cast(list[dict[str, str]], json.loads(content))

        if faculty:
            return [c["prefix"] for c in data if c["faculty"] == faculty.value.upper()]
        return [c["prefix"] for c in data]

    def close(self):
        self.client.close()
