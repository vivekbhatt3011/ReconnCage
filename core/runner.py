import subprocess
from pathlib import Path


class Runner:
    def __init__(self, logger=None):
        self.logger = logger

    # =========================
    # SYNCHRONOUS EXECUTION
    # =========================
    def run(self, command: str, output_file: Path):
        """
        Run command synchronously and store output.
        """

        if self.logger:
            self.logger.info(f"Running: {command}")

        try:
            process = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            # Write stdout
            with open(output_file, "w") as f:
                f.write(process.stdout)

            # Append stderr if exists
            if process.stderr:
                with open(output_file, "a") as f:
                    f.write("\n[ERROR]\n" + process.stderr)

            if self.logger:
                self.logger.success(f"Completed: {command}")

            return process.stdout

        except Exception as e:
            if self.logger:
                self.logger.error(f"Execution failed: {str(e)}")
            return ""

    # =========================
    # BACKGROUND EXECUTION
    # =========================
    def run_background(self, command: str, output_file: Path):
        """
        Run command in background (non-blocking).
        """

        if self.logger:
            self.logger.info(f"[BG] Starting: {command}")

        try:
            outfile = open(output_file, "w")

            process = subprocess.Popen(
                command,
                shell=True,
                stdout=outfile,
                stderr=subprocess.PIPE,
                text=True
            )

            return process

        except Exception as e:
            if self.logger:
                self.logger.error(f"Background execution failed: {str(e)}")
            return None

    # =========================
    # WAIT HANDLER
    # =========================
    def wait(self, process):
        """
        Wait for background process safely.
        """

        try:
            process.wait()

            if self.logger:
                self.logger.success("Background task completed")

            return True

        except Exception as e:
            if self.logger:
                self.logger.error(f"Wait failed: {str(e)}")
            return False

    # =========================
    # TOOL CHECK
    # =========================
    def check_tool(self, tool_name: str):
        """
        Check if tool exists in PATH.
        """

        result = subprocess.run(
            f"which {tool_name}",
            shell=True,
            capture_output=True,
            text=True
        )

        return result.returncode == 0