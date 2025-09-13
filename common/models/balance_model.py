from decimal import Decimal
from typing import List, Any, Dict

from pydantic import BaseModel

from common.constants import TWODIGITS


class Balance(BaseModel):
    date: str
    total: Decimal
    dayBalance: Decimal

    def model_dump(self) -> dict[str, Any]:
        return {
            "date": self.date[0:10],
            "total": self.total.quantize(TWODIGITS),
            "dayBalance": self.dayBalance.quantize(TWODIGITS),
        }

