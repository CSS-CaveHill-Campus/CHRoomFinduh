from pydantic import BaseModel


class FreeRoom(BaseModel):
    room: str
    available_from: int
    available_to: int
