import datetime
from pathlib import Path


class Logger:
    def __init__(self, logfile: Path):
        self.logfile = logfile

    def _write(self, level: str, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"

        # Print to console
        print(log_entry)

        # Write to file
        with open(self.logfile, "a") as f:
            f.write(log_entry + "\n")

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