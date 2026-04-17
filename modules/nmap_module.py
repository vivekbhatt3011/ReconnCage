import subprocess
import re
from pathlib import Path
from utils import log, save_output, mark_done, is_done

MODULE_P1 = "nmap_phase1"
MODULE_P2 = "nmap_phase2"

def parse_open_ports(nmap_output: str) -> list:
    """Extract open ports from nmap output."""
    ports = []
    for line in nmap_output.splitlines():
        match = re.match(r"(\d+)/tcp\s+open", line)
        if match:
            ports.append(match.group(1))
    return ports


def run_phase1(domain: str, output_dir: Path, profile: dict, scope: list, live_hosts: list) -> list:
    """Phase 1: Fast surface scan. Returns list of open ports found."""

    if is_done(output_dir, MODULE_P1):
        log(output_dir, f"[nmap] Phase 1 already completed. Skipping.", "WARNING")
        out_file = output_dir / "nmap_phase1.txt"
        if out_file.exists():
            with open(out_file) as f:
                return parse_open_ports(f.read())
        return []

    if not live_hosts:
        log(output_dir, f"[nmap] No live hosts for Phase 1. Skipping.", "WARNING")
        mark_done(output_dir, MODULE_P1)
        return []

    # Extract clean hostnames
    clean_hosts = []
    for h in live_hosts:
        clean = h.replace("https://", "").replace("http://", "").split("/")[0]
        clean_hosts.append(clean)

    flags = profile.get("nmap_phase1_flags", "-T4 --top-ports 1000").split()
    targets = list(set(clean_hosts))

    log(output_dir, f"[nmap] Phase 1 started — fast surface scan on {len(targets)} hosts ({profile['nmap_phase1_flags']})")

    out_file = output_dir / "nmap_phase1.txt"

    try:
        cmd = ["nmap"] + flags + ["-oN", str(out_file)] + targets
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        output = result.stdout
        with open(out_file, "w") as f:
            f.write(output)

        open_ports = parse_open_ports(output)
        log(output_dir, f"[nmap] Phase 1 complete. Open ports found: {', '.join(open_ports) if open_ports else 'none'}. Saved to nmap_phase1.txt", "SUCCESS")

    except subprocess.TimeoutExpired:
        log(output_dir, f"[nmap] Phase 1 timed out", "ERROR")
        open_ports = []
    except Exception as e:
        log(output_dir, f"[nmap] Phase 1 error: {str(e)}", "ERROR")
        open_ports = []

    mark_done(output_dir, MODULE_P1)
    return open_ports


def run_phase2(domain: str, output_dir: Path, profile: dict, scope: list, live_hosts: list, open_ports: list):
    """Phase 2: Detailed scan on open ports only."""

    if is_done(output_dir, MODULE_P2):
        log(output_dir, f"[nmap] Phase 2 already completed. Skipping.", "WARNING")
        return

    if not open_ports:
        log(output_dir, f"[nmap] No open ports from Phase 1. Skipping Phase 2.", "WARNING")
        mark_done(output_dir, MODULE_P2)
        return

    if not live_hosts:
        log(output_dir, f"[nmap] No live hosts for Phase 2. Skipping.", "WARNING")
        mark_done(output_dir, MODULE_P2)
        return

    clean_hosts = []
    for h in live_hosts:
        clean = h.replace("https://", "").replace("http://", "").split("/")[0]
        clean_hosts.append(clean)

    ports_str = ",".join(open_ports)
    flags = profile.get("nmap_phase2_flags", "-T4 -sV -sC").split()
    targets = list(set(clean_hosts))

    log(output_dir, f"[nmap] Phase 2 started — detailed scan on ports {ports_str} ({profile['nmap_phase2_flags']})")

    out_file = output_dir / "nmap_phase2.txt"

    try:
        cmd = ["nmap"] + flags + ["-p", ports_str, "-oN", str(out_file)] + targets
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        with open(out_file, "w") as f:
            f.write(result.stdout)
        log(output_dir, f"[nmap] Phase 2 complete. Saved to nmap_phase2.txt", "SUCCESS")
    except subprocess.TimeoutExpired:
        log(output_dir, f"[nmap] Phase 2 timed out", "ERROR")
    except Exception as e:
        log(output_dir, f"[nmap] Phase 2 error: {str(e)}", "ERROR")

    mark_done(output_dir, MODULE_P2)
