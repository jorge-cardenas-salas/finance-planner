#!/usr/bin/env python3
"""
Finance Planner UI using NiceGUI
Allows users to upload schedules, configure simulation parameters, and download results.
"""

import csv
import io
import tempfile
from decimal import Decimal
from io import StringIO
from typing import List, Tuple, Optional

from nicegui import ui, app

from common.models.movement_model import Movement
from data_upload.parser import Parser
from simulator import Simulator
from datetime import datetime, timedelta
import logging

class FinancePlannerUI:
    def __init__(self):
        self.movements: List[Movement] = []
        self.balances = None
        self.html_output = None
        self.csv_buffer = None
        self.status_log = []
        self.uploaded_content: Optional[str] = None

    def log_status(self, message: str):
        """Add message to status log and update UI."""
        logger = logging.getLogger(__name__)
        logger.info(message, exc_info=True)

        self.status_log.append(message)
        # Update the UI textarea if it exists (UI may not be built at import time)
        if hasattr(self, 'status_display') and self.status_display:
            # NiceGUI textarea in 3.4.1 doesn't have set_text(); update .value instead
            self.status_display.value = "\n".join(self.status_log[-20:])

    def validate_inputs(self) -> Tuple[bool, str]:
        """Validate all user inputs before running simulation."""
        if not self.uploaded_content:
            return False, "❌ Please upload a schedules CSV file."

        try:
            start_amt = Decimal(str(self.start_amount.value))
            if start_amt < 0:
                return False, "❌ Initial balance must be non-negative."
        except (ValueError, TypeError):
            return False, "❌ Invalid initial balance amount."

        if not self.start_date.value or not self.end_date.value:
            return False, "❌ Please select both start and end dates."

        if self.start_date.value > self.end_date.value:
            return False, "❌ Start date must be before end date."

        return True, "✅ Inputs valid."

    async def on_file_upload(self, e):
        """Handle schedule CSV/TSV file upload (robust to different file shapes)."""
        file = getattr(e, "file", None)
        if file is None:
            self.log_status("No file found on event")
            return
        filename = getattr(file, "name", None)

        # Try common places where file bytes might live
        content_bytes = None
        # some NiceGUI versions store raw bytes in ._data (memoryview/bytes)
        data = getattr(file, "_data", None)
        if data is not None:
            if isinstance(data, memoryview):
                content_bytes = data.tobytes()
            elif isinstance(data, (bytes, bytearray)):
                content_bytes = bytes(data)
            elif isinstance(data, str):
                # sometimes incorrectly provided as str — decode safely
                content_bytes = data.encode("utf-8")
            else:
                # fallback: try to get bytes()
                try:
                    content_bytes = bytes(data)
                except Exception:
                    content_bytes = None

        # Some file objects provide an async read() or .read() method
        if content_bytes is None:
            read_fn = getattr(file, "read", None)
            if callable(read_fn):
                # if it's async
                try:
                    maybe = read_fn()
                    if getattr(maybe, "__await__", None):
                        content_bytes = await maybe
                    else:
                        content_bytes = maybe
                except TypeError:
                    # read might require args, ignore
                    content_bytes = None

            if content_bytes is None:
                self.log_status("❌ Could not read uploaded file bytes.")
                return

        # Ensure we have actual bytes
        if isinstance(content_bytes, str):
            content_bytes = content_bytes.encode("utf-8")
        elif isinstance(content_bytes, memoryview):
            content_bytes = content_bytes.tobytes()

        # Strip UTF-8 BOM if present
        if content_bytes.startswith(b"\xef\xbb\xbf"):
            content_bytes = content_bytes[3:]

        # Decode to text
        try:
            content_str = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            # fallback with replacement to avoid crashes
            content_str = content_bytes.decode("utf-8", errors="replace")

        # Use csv to parse TSV (more robust than manual split)
        buf = io.StringIO(content_str)
        reader = csv.DictReader(buf, delimiter="\t")
        if reader.fieldnames is None:
            self.log_status("❌ Empty file or invalid TSV.")
            return

        headers = set(fn.strip() for fn in reader.fieldnames)
        expected = {"Description", "Amount", "Start", "End", "Frequency", "Type"}
        if headers != expected:
            self.log_status(f"❌ CSV headers incorrect.\nExpected: {expected}\nGot: {headers}")
            return

        self.uploaded_content = content_str
        self.log_status(f"✅ File uploaded and validated: {filename or 'uploaded file'}")

    async def run_simulation(self):
        """Execute the full pipeline: parse → generate movements → simulate → export."""
        is_valid, msg = self.validate_inputs()
        if not is_valid:
            self.log_status(msg)
            return

        self.run_button.enabled = False
        # Clear status display
        self.status_display.value = ""
        self.status_log.clear()

        try:
            # 1. Parse schedules from uploaded content
            self.log_status("📂 Parsing schedules file...")
            
            # Write uploaded content to temp file
            # Ensure uploaded_content is a str before writing to a text temp file
            content_str = self.uploaded_content
            assert isinstance(content_str, str)
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
                tmp.write(content_str)
                tmp_path = tmp.name

            parser = Parser()
            success, schedules = parser.uploadSchedules(tmp_path)
            if not success or not schedules:
                self.log_status("❌ Failed to parse schedules. Check file format and headers.")
                return

            self.log_status(f"✅ Parsed {len(schedules)} schedules.")

            # 2. Generate movements
            self.log_status("📋 Generating movements...")
            self.movements = []
            for schedule in schedules:
                movements = schedule.generateMovements(
                    start=str(self.start_date.value),
                    end=str(self.end_date.value)
                )
                self.movements.extend(movements)

            self.movements.sort(key=lambda mov: (mov.date, mov.amount))
            self.log_status(f"✅ Generated {len(self.movements)} movements.")

            # 3. Create movements CSV (optional)
            if self.create_movements_file.value:
                self.log_status("💾 Creating movements CSV...")
                movement_list = [mov.model_dump() for mov in self.movements]
                keys = list(movement_list[0].keys()) if movement_list else []

                # Store in buffer for download
                csv_lines = ["\t".join(keys)]
                for mov in movement_list:
                    csv_lines.append("\t".join(str(mov[k]) for k in keys))
                self.csv_buffer = "\n".join(csv_lines)
                self.log_status("✅ Movements CSV ready for download.")

            # 4. Run simulation (optional)
            if self.run_simulation_flag.value:
                self.log_status("⚙️ Running simulation...")
                simulator = Simulator()
                self.balances = simulator.simulate(
                    movements=self.movements,
                    startAmount=Decimal(str(self.start_amount.value)),
                    startDate=str(self.start_date.value)
                )
                self.log_status(f"✅ Simulation complete ({len(self.balances)} daily balances).")

                # Generate HTML
                self.log_status("📊 Generating HTML report...")
                self.html_output = simulator.writeHtml(output_path=None)
                self.log_status("✅ HTML report ready for download.")

            self.log_status("🎉 Pipeline complete! Download results below.")

        except Exception as ex:
            self.log_status(f"❌ Error: {str(ex)}")
        finally:
            self.run_button.enabled = True

    def build_ui(self):
        """Build the NiceGUI interface."""
        with ui.column().classes('w-full max-w-2xl mx-auto p-6'):
            ui.label("📊 Finance Planner").classes('text-3xl font-bold mb-6')

            # Section 1: Upload schedules
            with ui.card().classes('w-full'):
                ui.label("1️⃣ Upload Schedules File").classes('text-lg font-semibold')
                ui.label(
                    "CSV file must be tab-delimited with headers: Description, Amount, Start, End, Frequency, Type"
                ).classes('text-sm text-gray-600 mb-2')

                self.uploaded_file = ui.upload(
                    on_upload=self.on_file_upload,
                    multiple=False
                ).props('accept=".csv" max-file-size=10485760')

                ui.button(
                    "📥 Download CSV Template",
                    on_click=lambda: ui.download(
                        "Description\tAmount\tStart\tEnd\tFrequency\tType\nSalary\t5000.00\t2025-09-01\t2026-12-31\tMONTHLY\tINCOME\nRent\t1200.00\t2025-09-01\t2026-12-31\tMONTHLY\tEXPENSE",
                        filename="schedule_template.csv"
                    )
                ).props('color=info')

            # Section 2: Configure simulation
            with ui.card().classes('w-full'):
                ui.label("2️⃣ Simulation Parameters").classes('text-lg font-semibold')

                with ui.row().classes('w-full gap-4'):
                    today = datetime.now().date().isoformat()
                    one_year_later = (datetime.now().date() + timedelta(days=365)).isoformat()
                    
                    self.start_date = ui.input(
                        label="Start Date",
                        value=today,
                        placeholder="yyyy-mm-dd"
                    ).classes('flex-1').props('type=date')
                    
                    self.end_date = ui.input(
                        label="End Date",
                        value=one_year_later,
                        placeholder="yyyy-mm-dd"
                    ).classes('flex-1').props('type=date')

                self.start_amount = ui.number(
                    label="Initial Balance ($)",
                    value=1894.17,
                    min=0,
                    step=0.01
                ).classes('w-full')

            # Section 3: Options
            with ui.card().classes('w-full'):
                ui.label("3️⃣ Options").classes('text-lg font-semibold')

                self.create_movements_file = ui.checkbox(
                    "Create movements CSV file",
                    value=True
                )

                self.run_simulation_flag = ui.checkbox(
                    "Run simulation & generate HTML report",
                    value=True
                )

            # Section 4: Run and download
            with ui.card().classes('w-full'):
                ui.label("4️⃣ Execute & Download").classes('text-lg font-semibold')

                self.run_button = ui.button(
                    "▶️ Run Simulation",
                    on_click=self.run_simulation
                ).props('color=primary').classes('w-full')

                with ui.row().classes('w-full gap-2'):
                    ui.button(
                        "⬇️ Download Movements CSV",
                        on_click=lambda: self._download_csv() if self.csv_buffer else ui.notify("No CSV to download. Run simulation first.", type="warning")
                    ).props('color=info')

                    ui.button(
                        "⬇️ Download HTML Report",
                        on_click=lambda: self._download_html() if self.html_output else ui.notify("No HTML report to download. Run simulation first.", type="warning")
                    ).props('color=info')

            # Section 5: Status log
            with ui.card().classes('w-full'):
                ui.label("📋 Status Log").classes('text-lg font-semibold')
                self.status_display = ui.textarea(
                    value="Ready to upload schedules and configure simulation."
                ).props('readonly').classes('w-full h-48 text-sm font-mono')

    def _download_csv(self):
        """Download movements CSV."""
        try:
            if self.csv_buffer:
                # Convert the CSV string to bytes
                csv_bytes = self.csv_buffer.encode('utf-8')
                ui.download(csv_bytes, filename="movements.csv")
        except Exception as ex:
            self.log_status(f"❌ Error downloading CSV: {str(ex)}")

    def _download_html(self):
        """Download HTML report."""
        try:
            if self.html_output:
                html_bytes = self.html_output.encode('utf-8')
                ui.download(html_bytes, filename="daySummary.html")
        except Exception as ex:
            self.log_status(f"❌ Error downloading HTML: {str(ex)}")


# Create a global UI instance
planner_ui = FinancePlannerUI()


@ui.page('/')
async def index():
    """Main page — build the UI when accessed."""
    planner_ui.build_ui()


if __name__ in {"__main__", "__mp_main__"}:
    # Start the builtin server when executed directly (for development)
    ui.run(title="Finance Planner", port=8080)



