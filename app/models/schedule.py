from pydantic import BaseModel

from app.schemas.enums import ClassTypeEnum, DayEnum


class Schedule(BaseModel):
    course_code: str
    day: DayEnum
    start_time: int
    end_time: int
    start_date: str  # mm/dd/yyyy
    end_date: str  # mm/dd/yyyy
    class_type: ClassTypeEnum
    room: str
    building: str
