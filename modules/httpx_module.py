import subprocess
import json
from pathlib import Path
from utils import log, save_output, mark_done, is_done

MODULE = "httpx"

def run(domain: str, output_dir: Path, profile: dict, scope: list, subdomains: list) -> tuple:
    """Returns (live_hosts, dead_hosts)"""

    if is_done(output_dir, MODULE):
        log(output_dir, f"[{MODULE}] Already completed. Skipping.", "WARNING")
        live_file = output_dir / "live_hosts.txt"
        dead_file = output_dir / "dead_hosts.txt"
        live = []
        dead = []
        if live_file.exists():
            with open(live_file) as f:
                live = [l.strip() for l in f if l.strip()]
        if dead_file.exists():
            with open(dead_file) as f:
                dead = [l.strip() for l in f if l.strip()]
        return live, dead

    if not subdomains:
        log(output_dir, f"[httpx] No subdomains to probe. Skipping.", "WARNING")
        mark_done(output_dir, MODULE)
        return [], []

    log(output_dir, f"[httpx] Probing {len(subdomains)} subdomains for live hosts")

    input_file = output_dir / "subdomains.txt"
    json_out = output_dir / "httpx_results.json"

    try:
        result = subprocess.run(
            [
                "httpx",
                "-l", str(input_file),
                "-json",
                "-o", str(json_out),
                "-silent",
                "-follow-redirects",
                "-status-code",
                "-title",
                "-tech-detect",
            ],
            capture_output=True, text=True, timeout=300
        )

        live_hosts = []
        if json_out.exists():
            with open(json_out) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        url = entry.get("url", "")
                        if url:
                            live_hosts.append(url)
                    except json.JSONDecodeError:
                        continue

        all_subdomains = set(subdomains)
        live_set = set()
        for h in live_hosts:
            for s in all_subdomains:
                if s in h:
                    live_set.add(s)

        dead_hosts = list(all_subdomains - live_set)

        save_output(output_dir, "live_hosts.txt", "\n".join(live_hosts))
        save_output(output_dir, "dead_hosts.txt", "\n".join(dead_hosts))

        log(output_dir, f"[httpx] Live: {len(live_hosts)} | Dead: {len(dead_hosts)}. Saved to live_hosts.txt and dead_hosts.txt", "SUCCESS")

    except subprocess.TimeoutExpired:
        log(output_dir, f"[httpx] Timed out", "ERROR")
        live_hosts, dead_hosts = [], []
    except Exception as e:
        log(output_dir, f"[httpx] Error: {str(e)}", "ERROR")
        live_hosts, dead_hosts = [], []

    mark_done(output_dir, MODULE)
    return live_hosts, dead_hosts
