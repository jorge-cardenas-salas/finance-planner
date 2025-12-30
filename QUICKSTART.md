# Quick Start Guide

Get the Finance Planner UI running in 3 steps:

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Start the UI

```bash
python ui.py
```

## 3. Open in Browser

The UI will automatically open at:
```
http://localhost:8080
```

## Using the App

### Example Workflow

1. **Download Template** → Click "📥 Download CSV Template" to get the format
2. **Create Schedule File** → Edit the template with your payment schedules
3. **Upload** → Click upload and select your CSV file
4. **Configure** → Set start date, end date, and initial balance
5. **Run** → Click "▶️ Run Simulation"
6. **Download** → Save the CSV and HTML results

### CSV Format (Tab-Delimited)

```
Description	Amount	Start	End	Frequency	Type
Salary	5000.00	2025-09-01	2026-12-31	MONTHLY	INCOME
Rent	1200.00	2025-09-01	2026-12-31	MONTHLY	EXPENSE
Utilities	150.00	2025-09-01	2026-12-31	MONTHLY	EXPENSE
```

### Key Notes

- **Tab-delimited only** (not comma-delimited)
- **Dates in ISO format**: YYYY-MM-DD
- **Frequency**: MONTHLY, WEEKLY, BIWEEKLY, QUARTERLY, BIMONTHLY, SINGLE
- **Type**: INCOME or EXPENSE

## Troubleshooting

- **Port 8080 in use?** Edit `ui.py`, change `ui.run(port=8080)` to another port
- **Module not found?** Ensure you ran `pip install -r requirements.txt`
- **CSV upload fails?** Check that the file is tab-delimited and has all required columns

## Full Documentation

See [README.md](README.md) for complete feature documentation and troubleshooting.
