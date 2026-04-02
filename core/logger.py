import datetime
from pathlib import Path


class Logger:
    def __init__(self, log_file: Path):
        self.log_file = log_file

        # Ensure parent directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    # =========================
    # INTERNAL WRITER
    # =========================
    def _write(self, level: str, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}"

        # Console output
        print(entry)

        # File output
        with open(self.log_file, "a") as f:
            f.write(entry + "\n")

    # =========================
    # LOG LEVELS
    # =========================
    def info(self, message: str):
        self._write("INFO", message)

    def success(self, message: str):
        self._write("SUCCESS", message)

    def warning(self, message: str):
        self._write("WARNING", message)

    def error(self, message: str):
        self._write("ERROR", message)

    # =========================
    # SPECIAL HELPERS
    # =========================
    def start_phase(self, phase_name: str):
        self.info(f"===== START: {phase_name} =====")

    def end_phase(self, phase_name: str):
        self.success(f"===== END: {phase_name} =====")