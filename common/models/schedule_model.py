from datetime import datetime
from decimal import Decimal
from typing import List

# import dateutil.parser
from dateutil import parser

from pydantic import BaseModel, Field

from common.constants import FrequencyType, MovementType, TWODIGITS, HOLIDAYS
from common.models.movement_model import Movement
from pandas import DateOffset


class Schedule(BaseModel):
    description: str = Field()
    amount: Decimal = Field()
    start: str = Field()
    end: str = Field()
    freq: FrequencyType = Field()
    movementType: MovementType = Field()
    movements: List[Movement] = Field(default=[])

    def generateMovements(self, start: str, end: str):
        wholeProgramStart = parser.isoparse(start)
        wholeProgramEnd = parser.isoparse(end)
        scheduleStart = parser.isoparse(self.start)
        scheduleEnd = parser.isoparse(self.end)

        if scheduleStart > wholeProgramEnd or scheduleEnd < wholeProgramStart:
            return self.movements or []

        nextOccurrence = scheduleStart

        while nextOccurrence <= scheduleEnd and nextOccurrence <= wholeProgramEnd:
            append = wholeProgramStart <= nextOccurrence <= wholeProgramEnd
            if append:
                movDict = {
                    "date": self.adjustBusinessDay(nextOccurrence).isoformat(),
                    "description": self.description,
                    "amount": self.amount * self.movementType.value
                }
                self.movements.append(Movement(**movDict))

            # Calculate next occurrence
            match self.freq:
                case FrequencyType.SINGLE:
                    break
                case FrequencyType.MONTHLY:
                    nextOccurrence = nextOccurrence + DateOffset(months=1)
                case FrequencyType.WEEKLY:
                    nextOccurrence = nextOccurrence + DateOffset(weeks=1)
                case FrequencyType.BIWEEKLY:
                    nextOccurrence = nextOccurrence + DateOffset(weeks=2)
                case FrequencyType.QUARTERLY:
                    nextOccurrence = nextOccurrence + DateOffset(months=3)
                case FrequencyType.BIMONTHLY:
                    nextOccurrence = nextOccurrence + DateOffset(months=2)

        return self.movements or []

    def getMovements(self):
        return self.movements

    @staticmethod
    def adjustBusinessDay(date: datetime) -> datetime:
        while date.weekday() in [5, 6] or date in HOLIDAYS:
            date = date - DateOffset(days=1)

        return date
