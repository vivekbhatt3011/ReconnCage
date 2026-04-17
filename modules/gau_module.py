import subprocess
from pathlib import Path
from utils import log, save_output, mark_done, is_done

MODULE = "gau"

def run(domain: str, output_dir: Path, profile: dict, scope: list):
    if is_done(output_dir, MODULE):
        log(output_dir, f"[{MODULE}] Already completed. Skipping.", "WARNING")
        return

    log(output_dir, f"[gau] Fetching historical URLs for {domain}")

    out_file = output_dir / "gau_urls.txt"

    try:
        result = subprocess.run(
            ["gau", "--subs", domain],
            capture_output=True, text=True, timeout=300
        )
        urls = [l.strip() for l in result.stdout.splitlines() if l.strip()]
        save_output(output_dir, "gau_urls.txt", "\n".join(urls))
        log(output_dir, f"[gau] Found {len(urls)} historical URLs. Saved to gau_urls.txt", "SUCCESS")
    except subprocess.TimeoutExpired:
        log(output_dir, f"[gau] Timed out", "ERROR")
    except Exception as e:
        log(output_dir, f"[gau] Error: {str(e)}", "ERROR")

    mark_done(output_dir, MODULE)
