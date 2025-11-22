from pydantic import BaseModel

from app.schemas.enums import DayEnum


class Schedule(BaseModel):
    course_code: str
    day: DayEnum
    start_time: int
    end_time: int
    class_type: str
    start_date: str  # mm/dd/yyyy
    end_date: str  # mm/dd/yyyy
    room: str
    building: str
