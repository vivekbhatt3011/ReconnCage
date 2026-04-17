import subprocess
import os
from pathlib import Path
from utils import log, save_output, mark_done, is_done

MODULE = "ffuf"

WORDLIST_PATH = Path(__file__).parent.parent / "wordlists" / "big.txt"


def run(domain: str, output_dir: Path, profile: dict, scope: list, live_hosts: list):
    if is_done(output_dir, MODULE):
        log(output_dir, f"[{MODULE}] Already completed. Skipping.", "WARNING")
        return

    if not live_hosts:
        log(output_dir, f"[ffuf] No live hosts. Skipping.", "WARNING")
        mark_done(output_dir, MODULE)
        return

    if not WORDLIST_PATH.exists():
        log(output_dir, f"[ffuf] Wordlist not found at {WORDLIST_PATH}. Please add wordlists/big.txt to the framework directory.", "ERROR")
        mark_done(output_dir, MODULE)
        return

    threads     = profile.get("ffuf_threads", 100)
    depth       = profile.get("ffuf_recursive_depth", 0)
    ffuf_outdir = output_dir / "ffuf"
    ffuf_outdir.mkdir(exist_ok=True)

    log(output_dir, f"[ffuf] Starting directory brute-force on {len(live_hosts)} hosts (threads: {threads}, recursive depth: {depth})")

    for host in live_hosts:
        host_clean = host.replace("https://", "").replace("http://", "").split("/")[0].replace(".", "_")
        out_file = ffuf_outdir / f"{host_clean}.txt"

        cmd = [
            "ffuf",
            "-u", f"{host}/FUZZ",
            "-w", str(WORDLIST_PATH),
            "-t", str(threads),
            "-mc", "200,201,204,301,302,307,401,403",
            "-o", str(out_file),
            "-of", "json",
            "-s",
        ]

        if depth > 0:
            cmd += ["-recursion", "-recursion-depth", str(depth)]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            log(output_dir, f"[ffuf] Completed on {host}. Output saved.", "SUCCESS")
        except subprocess.TimeoutExpired:
            log(output_dir, f"[ffuf] Timeout on {host}", "WARNING")
        except Exception as e:
            log(output_dir, f"[ffuf] Error on {host}: {str(e)}", "ERROR")

    log(output_dir, f"[ffuf] All hosts complete. Results in ffuf/ directory", "SUCCESS")
    mark_done(output_dir, MODULE)
