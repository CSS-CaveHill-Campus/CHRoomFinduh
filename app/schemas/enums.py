"""All enums used by the application will be here!"""

from enum import Enum


class StatusEnum(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class FacultyEnum(str, Enum):
    FCCPA = "FCCPA"
    FHE = "FHE"
    LAW = "LAW"
    FMS = "FMS"
    FST = "FST"
    FSS = "FSS"


class DayEnum(str, Enum):
    MON = "mon"
    TUE = "tue"
    WED = "wed"
    THU = "thu"
    FRI = "fri"
    SAT = "sat"
    SUN = "sun"
    ALL = "all"
