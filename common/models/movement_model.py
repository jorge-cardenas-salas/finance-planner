from decimal import Decimal
from typing import Any

from pydantic import BaseModel

from common.constants import TWODIGITS


class Movement(BaseModel):
    date: str
    description: str
    amount: Decimal

    def model_dump(self) -> dict[str, Any]:
        return {
            "description": self.description,
            "date": self.date[0:10],
            "amount": self.amount.quantize(TWODIGITS),
        }
