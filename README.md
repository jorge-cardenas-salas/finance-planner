# finance-planner

A Python application for financial planning and movement simulation. Upload recurring payment schedules, generate daily cash flow projections, and export results.

## Features

- 📂 **Upload Schedule Files**: CSV-based payment schedules with recurring frequency (monthly, weekly, biweekly, quarterly, bimonthly, single)
- 📊 **Simulate Cash Flow**: Calculate daily balances from a starting amount and movement transactions
- 💾 **Export Results**: Download generated movements (CSV) and daily balance reports (HTML)
- 🎨 **Web UI**: Simple, user-friendly NiceGUI interface

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Running the Web UI

Start the NiceGUI application:

```bash
python main.py
```

The UI will open at `http://localhost:8080` in your browser.

### Using the UI

1. **Upload Schedules File** (Section 1):
   - Click the upload button and select a tab-delimited CSV file
   - CSV must have headers: `Description`, `Amount`, `Start`, `End`, `Frequency`, `Type`
   - Download the template for reference: **📥 Download CSV Template**

2. **Set Simulation Parameters** (Section 2):
   - **Start Date**: First date for simulation
   - **End Date**: Last date for simulation
   - **Initial Balance ($)**: Starting account balance

3. **Configure Options** (Section 3):
   - ☑️ **Create movements CSV file**: Export list of all movements
   - ☑️ **Run simulation & generate HTML report**: Calculate daily balances and create an HTML report

4. **Execute & Download** (Section 4):
   - Click **▶️ Run Simulation** to process your data
   - Status messages appear in the log
   - Download results: **⬇️ Download Movements CSV** and **⬇️ Download HTML Report**

## CSV File Format

Your schedule file must be tab-delimited (not comma-delimited) with the following columns:

| Description | Amount | Start | End | Frequency | Type |
|---|---|---|---|---|---|
| Salary | 5000.00 | 2025-09-01 | 2026-12-31 | MONTHLY | INCOME |
| Rent | 1200.00 | 2025-09-01 | 2026-12-31 | MONTHLY | EXPENSE |
| Bonus | 2000.00 | 2025-12-15 | 2025-12-15 | SINGLE | INCOME |

**Frequency Options:**
- `MONTHLY`: Every month
- `WEEKLY`: Every week
- `BIWEEKLY`: Every two weeks
- `QUARTERLY`: Every three months
- `BIMONTHLY`: Every two months
- `SINGLE`: One-time payment

**Type Options:**
- `INCOME`: Money coming in
- `EXPENSE`: Money going out

**Date Format:** ISO 8601 format (`YYYY-MM-DD`)

## Output Files

- **movements.csv**: Tab-delimited file with all generated movements (date, description, amount)
- **daySummary.html**: Formatted HTML report showing daily totals and running balance

## Technical Details

### Architecture

- **Parser** (`data_upload/parser.py`): Reads and validates schedule CSV files
- **Schedule** (`common/models/schedule_model.py`): Generates movement occurrences based on frequency; adjusts for business days (skips weekends and holidays)
- **Movement** (`common/models/movement_model.py`): Individual transaction record
- **Simulator** (`simulator.py`): Calculates daily balances and generates HTML reports
- **UI** (`main.py`): NiceGUI web interface for user interaction

### Business Day Adjustments

The simulator automatically adjusts payment dates to business days (skipping weekends and Mexican holidays for 2025-2026).

### Precision

All amounts are handled using Python's `Decimal` type for financial accuracy (2 decimal places).

## Dependencies

- **pandas**: Date arithmetic and offset calculations
- **pydantic**: Data model validation
- **python-dateutil**: Date parsing and manipulation
- **nicegui**: Web UI framework
- **python-multipart**: File upload handling
- **aiofiles**: Async file operations

## Troubleshooting

### CSV Upload Fails
- Ensure the file is tab-delimited (not comma-delimited)
- Check that all required columns are present: `Description`, `Amount`, `Start`, `End`, `Frequency`, `Type`
- Verify dates are in ISO format (`YYYY-MM-DD`)
- Check that `Frequency` and `Type` values match exactly (case-sensitive)

### Simulation Produces No Results
- Ensure schedule start/end dates overlap with simulation start/end dates
- Check that at least one checkbox is enabled (Create CSV or Run Simulation)
- Review the Status Log for error messages

### UI Won't Load
- Verify port 8080 is not in use: `lsof -i :8080`
- Try a different port by modifying the `ui.run(port=8080)` line in `main.py`
- Check that all dependencies are installed: `pip install -r requirements.txt`


## License

This project is for personal use.


# Terms
* `Schedule`: A list of recurring payments, with fields:
    * `Description`
    * `Amount`
    * `Start` (in format `yyyy-mm-dd`)
    * `End` (in format `yyyy-mm-dd`)
    * `Frequency` (`MONTHLY`,`WEEKLY`,`BIWEEKLY`,`QUARTERLY`,`BIMONTHLY`,`SINGLE`)
    `INCOME` and `EXPENSE`



    * `Type`
# Use Cases (Ideal State)
* Create a payment plan
    * User can upload a 

# Use Cases (Minimal for 2025-12-29)
**WHAT I NEED RIGHT NOW** is to be able to see if I will be able to pay the overdue Telus amount, plus all of January (at least) without further transferences

Given the following payment program:
```
Description	Amount	Start	End	Frequency	Type
Car Insurance	463.38	2025-01-14	2025-02-14	MONTHLY	EXPENSE
Car Insurance	434.22	2025-03-14	2025-06-25	MONTHLY	EXPENSE
Car Insurance	631	2025-07-14	2025-09-13	MONTHLY	EXPENSE
Car Insurance	348.9	2025-09-15	2025-12-31	MONTHLY	EXPENSE
Cell phones (Telus)	265	2025-01-11	2025-12-31	MONTHLY	EXPENSE
Electricity	110	2025-01-17	2025-12-31	MONTHLY	EXPENSE
Gas	329.72	2025-02-17	2025-12-31	SINGLE	EXPENSE
Gas	146.09	2025-03-17	2025-12-31	SINGLE	EXPENSE
Gas	283.45	2025-04-17	2025-12-31	SINGLE	EXPENSE
Gas	143.47	2025-05-17	2025-12-31	SINGLE	EXPENSE
Gas	78.91	2025-06-17	2025-12-31	SINGLE	EXPENSE
Gas	54.5	2025-07-17	2025-12-31	SINGLE	EXPENSE
Gas	60	2025-08-17	2025-12-31	SINGLE	EXPENSE
Gas	71.67	2025-09-17	2025-12-31	SINGLE	EXPENSE
Gas	43.72	2025-10-17	2025-12-31	SINGLE	EXPENSE
Gas	118.72	2025-11-17	2025-12-31	SINGLE	EXPENSE
Gas	170.54	2025-12-17	2025-12-31	SINGLE	EXPENSE
Gas	228.07	2026-01-17	2025-12-31	SINGLE	EXPENSE
Gas	329.72	2026-02-17	2025-12-31	SINGLE	EXPENSE
Honda CRV	363.51	2025-01-31	2027-12-31	MONTHLY	EXPENSE
Subaru X-Trek	123.92	2025-03-13	2027-02-11	MONTHLY	EXPENSE
House Rent	3587.5	2025-01-31	2025-02-28	MONTHLY	EXPENSE
House Rent	3400	2025-03-01	2025-12-31	MONTHLY	EXPENSE
Internet (Rogers)	67.8	2025-01-12	2025-12-31	MONTHLY	EXPENSE
Purpose Cell Benefit	50	2025-02-03	2025-12-31	MONTHLY	INCOME
Rent Insurance (Unifund)	95.9	2025-01-05	2025-09-13	MONTHLY	EXPENSE
Rent Insurance (Scoop?)	28.37	2025-09-15	2025-12-31	MONTHLY	EXPENSE
Rocinante	235.4	2025-01-13	2025-01-28	SINGLE	EXPENSE
Transfer	2294	2025-01-15	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-01-31	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-02-14	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-02-28	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-03-14	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-03-31	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-04-14	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-04-30	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-05-14	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-05-30	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-06-13	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-06-30	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-07-14	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-07-31	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-08-14	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-08-29	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-09-12	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-09-29	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-10-14	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-10-31	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-11-14	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-11-28	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-12-12	2025-12-31	SINGLE	INCOME
Transfer	2294	2025-12-31	2025-12-31	SINGLE	INCOME
Transfer	2294	2026-01-14	2025-12-31	SINGLE	INCOME
Water	182	2025-02-20	2025-12-31	QUARTERLY	EXPENSE
WealthSimple Interest	3	2025-01-01	2025-12-31	MONTHLY	INCOME
Home Insurance Cancel	160	2025-08-30	2025-09-01	SINGLE	INCOME
Aixa	650	2025-10-01	2025-12-31	MONTHLY	EXPENSE
Aixa	325	2025-09-15	2025-09-16	SINGLE	EXPENSE
```


1. User copy/paste a tab-separated list of programmed money movements, with fields `Desc`, `Date` and `Amount`
2. User copy/paste a tab-separated list of actual money movements, with fields `Desc`, `Date` and `Amount`