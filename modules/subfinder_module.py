import subprocess
from pathlib import Path
from utils import log, save_output, mark_done, is_done, filter_scope

MODULE = "subfinder"

def run(domain: str, output_dir: Path, profile: dict, scope: list) -> list:
    if is_done(output_dir, MODULE):
        log(output_dir, f"[{MODULE}] Already completed. Skipping.", "WARNING")
        out_file = output_dir / "subdomains.txt"
        if out_file.exists():
            with open(out_file) as f:
                return [l.strip() for l in f if l.strip()]
        return []

    log(output_dir, f"[subfinder] Starting subdomain enumeration on {domain}")

    out_file = output_dir / "subdomains_raw.txt"

    try:
        result = subprocess.run(
            ["subfinder", "-d", domain, "-o", str(out_file), "-silent"],
            capture_output=True, text=True, timeout=300
        )
        if not out_file.exists():
            log(output_dir, f"[subfinder] No output generated", "WARNING")
            mark_done(output_dir, MODULE)
            return []

        with open(out_file) as f:
            subdomains = [l.strip() for l in f if l.strip()]

        # Scope filter
        if scope:
            subdomains = filter_scope(subdomains, scope)

        save_output(output_dir, "subdomains.txt", "\n".join(subdomains))
        log(output_dir, f"[subfinder] Found {len(subdomains)} subdomains (after scope filter). Saved to subdomains.txt", "SUCCESS")

    except subprocess.TimeoutExpired:
        log(output_dir, f"[subfinder] Timed out", "ERROR")
        subdomains = []
    except Exception as e:
        log(output_dir, f"[subfinder] Error: {str(e)}", "ERROR")
        subdomains = []

    mark_done(output_dir, MODULE)
    return subdomains
