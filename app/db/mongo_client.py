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
from app.models import RoomAvailability, Schedule, Room, Prefix


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
            query["course_code"] = {"$regex": f"^({'|'.join(faculty_prefixes)})"}
        if prefix:  # Prefix takes precedence
            query["course_code"] = {"$regex": f"^{prefix}"}

        cursor = self.schedule_collection.find(query, {"_id": 0})
        if limit > 0:
            cursor = cursor.limit(limit)

        return [
            Schedule.model_validate(item)
            for item in await cursor.to_list(length=limit if limit > 0 else None)
        ]

    async def get_all_rooms(self):
        async with aiofiles.open("app/public/rooms.json", mode="r") as f:
            content = await f.read()

        rooms: list[Room] = [
            Room.model_validate(item)
            for item in cast(list[dict[str, str]], json.loads(content))
        ]
        return rooms

    async def _get_sanitized_prefixes(self) -> list[Prefix]:
        async with aiofiles.open("app/public/prefixes.json", mode="r") as f:
            content = await f.read()

        data: list[Prefix] = [
            Prefix.model_validate(item)
            for item in cast(list[dict[str, str]], json.loads(content))
        ]

        return data

    async def get_prefixes(self, faculty: FacultyEnum | None = None) -> list[str]:
        results: list[Prefix] = await self._get_sanitized_prefixes()
        if faculty:
            return [c.prefix for c in results if c.faculty == faculty.value.upper()]
        return [c.prefix for c in results]

    async def get_prefix_details(
        self, faculty: FacultyEnum | None = None
    ) -> list[Prefix]:
        results = await self._get_sanitized_prefixes()

        if faculty:
            return [c for c in results if c.faculty == faculty.value]
        return results

    async def get_room_availabilities(
        self,
        day: DayEnum,
        hour: int | None = None,
        duration: int | None = None,
        room: str | None = None,
    ) -> list[RoomAvailability]:
        query: dict[str, object] = {"day": day.value}

        if hour:
            query["available_from"] = hour
            query["available_to"] = {"$gte": hour + (duration or 1)}

        if room:
            query["room"] = room

        cursor = self.room_availabilities_collection.find(query, {"_id": 0})
        pipeline = [
            {"$match": query},
            {
                "$lookup": {
                    "from": "Rooms",  # Rooms collection name
                    "localField": "room",  # field from Free Rooms collection
                    "foreignField": "room",  # matching field in Rooms collection
                    "as": "room_info",  # output array field
                }
            },
            {"$unwind": "$room_info"},
            {
                "$project": {
                    "_id": 0,
                    "room": 1,
                    "day": 1,
                    "available_from": 1,
                    "available_to": 1,
                    "building": "$room_info.building",
                }
            },
        ]

        cursor = self.room_availabilities_collection.aggregate(pipeline)
        results = await cursor.to_list()

        return [RoomAvailability.model_validate(item) for item in results]

    def close(self):
        self.client.close()
