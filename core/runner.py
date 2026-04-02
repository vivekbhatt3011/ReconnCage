import subprocess
from pathlib import Path


def run_command(command: str, output_file: Path):
    """
    Run a command synchronously and save output.
    """

    try:
        process = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        # Save stdout
        with open(output_file, "w") as f:
            f.write(process.stdout)

        # Append stderr if exists
        if process.stderr:
            with open(output_file, "a") as f:
                f.write("\n[ERROR]\n" + process.stderr)

        return process.stdout

    except Exception as e:
        return f"[EXCEPTION] {str(e)}"


def run_command_background(command: str, output_file: Path):
    """
    Run a command in background (non-blocking).
    """

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
        print(f"[ERROR] Failed to start background process: {e}")
        return None


def wait_for_process(process):
    """
    Wait for a background process to complete safely.
    """

    try:
        process.wait()
        return True
    except Exception as e:
        print(f"[ERROR] Failed while waiting: {e}")
        return False


def check_tool_exists(tool_name: str):
    """
    Check if a tool exists in system PATH.
    """

    result = subprocess.run(
        f"which {tool_name}",
        shell=True,
        capture_output=True,
        text=True
    )

    return result.returncode == 0