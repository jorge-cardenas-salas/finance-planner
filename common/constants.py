import os
from decimal import Decimal
from enum import Enum, auto

from dateutil.parser import isoparse


class MovementType(Enum):
    INCOME = 1
    EXPENSE = -1


class FrequencyType(Enum):
    MONTHLY = auto()
    WEEKLY = auto()
    BIWEEKLY = auto()
    QUARTERLY = auto()
    BIMONTHLY = auto()
    SINGLE = auto()


TWODIGITS = Decimal(10) ** -2

HOLIDAYS = [
    isoparse("2025-01-01"),
    isoparse("2025-02-17"),
    isoparse("2025-04-18"),
    isoparse("2025-04-21"),
    isoparse("2025-05-19"),
    isoparse("2025-07-01"),
    isoparse("2025-08-04"),
    isoparse("2025-09-01"),
    isoparse("2025-10-13"),
    isoparse("2025-11-11"),
    isoparse("2025-12-25"),
    isoparse("2025-12-26"),
    isoparse("2026-01-01"),
]

PROJECT_NAME = os.getenv('PROJECT_NAME')

# Format to be used by the logger
DEFAULT_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(module)s.%(processName)s: %(message)s"
