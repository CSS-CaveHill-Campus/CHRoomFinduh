"""All enums used by the application will be here!"""

from enum import Enum


class StatusEnum(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class FacultyEnum(str, Enum):
    FCCPA = "fccpa"
    FHE = "fhe"
    LAW = "law"
    FMS = "fms"
    FST = "fst"
    FSS = "fss"


class DayEnum(str, Enum):
    MON = "mon"
    TUE = "tue"
    WED = "wed"
    THU = "thu"
    FRI = "fri"
    SAT = "sat"
    SUN = "sun"


class ClassTypeEnum(str, Enum):
    LECTURE = "l"
    TUTORIAL = "t"
