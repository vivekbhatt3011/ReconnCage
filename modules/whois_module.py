import subprocess
from pathlib import Path
from utils import log, save_output, mark_done, is_done

MODULE = "whois"

def run(domain: str, output_dir: Path, profile: dict, scope: list):
    if is_done(output_dir, MODULE):
        log(output_dir, f"[{MODULE}] Already completed. Skipping.", "WARNING")
        return

    log(output_dir, f"[whois] Starting whois lookup on {domain}")

    try:
        result = subprocess.run(
            ["whois", domain],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout if result.stdout else result.stderr
        save_output(output_dir, "whois.txt", output)
        log(output_dir, f"[whois] Completed. Output saved to whois.txt", "SUCCESS")
    except subprocess.TimeoutExpired:
        log(output_dir, f"[whois] Timed out on {domain}", "ERROR")
    except Exception as e:
        log(output_dir, f"[whois] Error: {str(e)}", "ERROR")

    mark_done(output_dir, MODULE)
