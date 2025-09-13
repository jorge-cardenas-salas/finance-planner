# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import csv
from csv import DictReader
from decimal import Decimal
from logging import Logger
from typing import List, Optional, Tuple, Dict

from pydantic import ValidationError

from common.constants import FrequencyType, MovementType
from common.models.schedule_model import Schedule
from common.utilities import DefaultLogger
from logging import Logger


class Parser:
    EXPECTED_HEADERS = {"Description", "Amount", "Start", "End", "Frequency", "Type"}

    def __init__(self, logger: Optional[Logger] = None):
        self.schedules: List[Schedule] = []
        self.success: bool = True
        self.logger: Logger = logger or DefaultLogger().get_logger()

    def uploadSchedules(self, filename: str) -> Tuple[bool, List[Schedule]]:
        # pass
        try:
            with open(filename, "r") as file:
                reader: DictReader = csv.DictReader(file, delimiter="\t")
                headers = set(reader.fieldnames)
                if headers != self.EXPECTED_HEADERS:
                    raise ValueError(f"Headers are incorrect, expected: {list(self.EXPECTED_HEADERS)}")

                for row in reader:
                    self.schedules.append(self.parseRow(row))

        except Exception as ex:
            self.logger.error(str(ex))
            self.success = False

        return self.success, self.schedules

    @staticmethod
    def parseRow(row: dict) -> Schedule:
        scheduleDict = {
            "description": row["Description"],
            "amount": Decimal(row["Amount"].strip(' "')),
            "start": row["Start"],
            "end": row["End"],
            "freq": FrequencyType[row["Frequency"]],
            "movementType": MovementType[row["Type"]]
        }
        return Schedule(**scheduleDict)
