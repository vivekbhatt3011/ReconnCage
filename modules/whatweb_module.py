import subprocess
from pathlib import Path
from utils import log, save_output, mark_done, is_done

MODULE = "whatweb"

def run(domain: str, output_dir: Path, profile: dict, scope: list, live_hosts: list):
    if is_done(output_dir, MODULE):
        log(output_dir, f"[{MODULE}] Already completed. Skipping.", "WARNING")
        return

    if not live_hosts:
        log(output_dir, f"[whatweb] No live hosts. Skipping.", "WARNING")
        mark_done(output_dir, MODULE)
        return

    log(output_dir, f"[whatweb] Fingerprinting tech stack on {len(live_hosts)} live hosts")

    results = []
    for host in live_hosts:
        try:
            result = subprocess.run(
                ["whatweb", "--color=never", "-a", "3", host],
                capture_output=True, text=True, timeout=30
            )
            output = result.stdout.strip()
            if output:
                results.append(output)
        except subprocess.TimeoutExpired:
            log(output_dir, f"[whatweb] Timeout on {host}", "WARNING")
        except Exception as e:
            log(output_dir, f"[whatweb] Error on {host}: {str(e)}", "ERROR")

    save_output(output_dir, "whatweb_results.txt", "\n".join(results))
    log(output_dir, f"[whatweb] Tech fingerprinting complete. Saved to whatweb_results.txt", "SUCCESS")

    mark_done(output_dir, MODULE)
