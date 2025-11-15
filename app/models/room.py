from pydantic import BaseModel


class Room(BaseModel):
    room: str
    available_from: int
    available_to: int
