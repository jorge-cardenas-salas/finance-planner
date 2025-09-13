from decimal import Decimal
from typing import List

from common.models.balance_model import Balance
from common.models.movement_model import Movement


class Simulator:
    def __init__(self):
        self.balances: List[Balance] = []

    def simulate(self, movements: List[Movement], startAmount: Decimal, startDate: str):
        output: List[Balance] = [Balance(**{
            "date": startDate,
            "total": 0,
            "dayBalance": startAmount,
        })]

        totals = self.dayTotals(movements=movements)
        currBalance = startAmount

        for date, amt in totals.items():
            entry = {
                "date": date,
                "total": amt,
                "dayBalance": currBalance + amt,
            }
            currBalance += amt
            output.append(Balance(**entry))

        self.balances = output
        return output

    def dayTotals(self, movements: List[Movement]) -> dict:
        totals = {}
        for movement in movements:
            totals[movement.date] = totals.get(movement.date, 0) + movement.amount

        sortedDates = list(totals.keys())
        sortedDates.sort()
        return {key: totals[key] for key in sortedDates}

    def writeHtml(self):
        balanceList = [bal.model_dump() for bal in self.balances]

        outFileName = "G:\\My Drive\\Finanzas\\2025\\daySummary.html"

        # Extract column names
        keys = list(balanceList[0].keys())

        # Generate HTML table with styles
        html_content = """<html>
        <head>
        <link rel="stylesheet" href="styles.css">
        <title>Day Summary</title>
        <style>
            body { font-family: Arial, sans-serif; }
            table { border-collapse: collapse; width: min(100%, 640px); }
            th, td { border: 1px solid black; padding: 8px; }
            th { background-color: #f2f2f2; text-align: center; }
            td { text-align: right; }
            .currency { text-align: right; white-space: nowrap; }
            .currency span { float: left; }
            .negative { background-color: #ffcccc; } /* Red background for negative values */
        </style>
        </head>
        <body>"""

        html_content += "<table>\n<tr>"

        # Write table headers
        html_content += "".join(f"<th>{key}</th>" for key in keys) + "</tr>\n"

        # Write table rows
        for row in balanceList:
            html_content += "<tr>"
            for i, key in enumerate(keys):
                value = row[key]
                cell_content = str(value)  # Default text

                if i in (1, 2):  # Format second and third columns as accounting style
                    formatted_value = f"({abs(value):,.2f})" if value < 0 else f"{value:,.2f}"
                    cell_content = f'<span>$</span>{formatted_value}'

                    # Add "currency" class for alignment
                    style = ' class="currency negative"' if i == 2 and value < 0 else ' class="currency"'
                else:
                    style = ""

                html_content += f"<td{style}>{cell_content}</td>"

            html_content += "</tr>\n"

        html_content += "</table>\n</body>\n</html>"

        # Save to file
        with open(outFileName, "w", encoding="utf-8") as outFile:
            outFile.write(html_content)
