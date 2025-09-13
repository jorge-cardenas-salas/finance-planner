# This is a sample Python script.
import csv
from decimal import Decimal
from typing import List

from common.models.movement_model import Movement
from data_upload.parser import Parser
from simulator import Simulator

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


if __name__ == '__main__':
    createMovementsFile: bool = True
    runSimulation: bool = True
    simulationStartAmount: Decimal = Decimal(4348.07)
    start = "2025-02-02"

    parser = Parser()
    success, schedules = parser.uploadSchedules(
        filename="G:\\My Drive\\Finanzas\\2025\\Sim1.csv"
    )
    movementList: List[dict] = []
    movementModels: List[Movement] = []
    allMovementModels: List[Movement] = []
    for schedule in schedules:
        movementModels = schedule.generateMovements(start=start, end="2026-01-01")
        movementList.extend([mov.model_dump() for mov in movementModels])
        allMovementModels.extend(movementModels)

    movementList.sort(key=lambda mov: (mov["date"], mov["amount"]))

    if createMovementsFile:
        outFileName = "G:\\My Drive\\Finanzas\\2025\\movements.csv"
        keys = list(movementList[0].keys())
        # keys = list(Movement.model_fields.keys())
        with open(outFileName, 'w', newline='') as outFile:
            dict_writer = csv.DictWriter(outFile, keys, delimiter="\t")
            dict_writer.writeheader()
            dict_writer.writerows(movementList)

    if runSimulation:
        simulator = Simulator()
        _ = simulator.simulate(
            movements=allMovementModels,
            startAmount=simulationStartAmount,
            startDate=start
        )
        simulator.writeHtml()
        # balanceList = [bal.model_dump() for bal in balanceModels]
        # outFileName = "G:\\My Drive\\Finanzas\\2025\\daySummary.csv"
        # keys = list(balanceList[0].keys())
        # with open(outFileName, 'w', newline='') as outFile:
        #     dict_writer = csv.DictWriter(outFile, keys, delimiter="\t")
        #     dict_writer.writeheader()
        #     dict_writer.writerows(balanceList)



