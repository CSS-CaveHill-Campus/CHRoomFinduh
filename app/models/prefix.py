from pydantic import BaseModel

from app.schemas.enums import FacultyEnum


class Prefix(BaseModel):
    faculty: FacultyEnum
    prefix: str
    desc: str

