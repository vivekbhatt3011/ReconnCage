import subprocess
from pathlib import Path
from utils import log, save_output, mark_done, is_done

MODULE = "dnsx"

def run(domain: str, output_dir: Path, profile: dict, scope: list, live_hosts: list):
    if is_done(output_dir, MODULE):
        log(output_dir, f"[{MODULE}] Already completed. Skipping.", "WARNING")
        return

    if not live_hosts:
        log(output_dir, f"[dnsx] No live hosts to resolve. Skipping.", "WARNING")
        mark_done(output_dir, MODULE)
        return

    log(output_dir, f"[dnsx] Starting DNS enumeration + SSL cert recon on {len(live_hosts)} live hosts")

    input_file = output_dir / "live_hosts.txt"
    dns_out    = output_dir / "dnsx_results.txt"
    ssl_out    = output_dir / "ssl_certs.txt"

    # DNS records
    try:
        result = subprocess.run(
            [
                "dnsx",
                "-l", str(input_file),
                "-a", "-aaaa", "-mx", "-txt", "-cname", "-ns",
                "-resp",
                "-o", str(dns_out),
                "-silent",
            ],
            capture_output=True, text=True, timeout=300
        )
        log(output_dir, f"[dnsx] DNS records saved to dnsx_results.txt", "SUCCESS")
    except subprocess.TimeoutExpired:
        log(output_dir, f"[dnsx] DNS enumeration timed out", "ERROR")
    except Exception as e:
        log(output_dir, f"[dnsx] DNS error: {str(e)}", "ERROR")

    # SSL cert enumeration via openssl
    ssl_results = []
    for host in live_hosts:
        host_clean = host.replace("https://", "").replace("http://", "").split("/")[0]
        try:
            result = subprocess.run(
                ["openssl", "s_client", "-connect", f"{host_clean}:443", "-servername", host_clean],
                input="",
                capture_output=True, text=True, timeout=10
            )
            output = result.stdout + result.stderr
            cert_lines = [l for l in output.splitlines() if any(k in l for k in ["subject=", "issuer=", "notBefore", "notAfter", "DNS:"])]
            if cert_lines:
                ssl_results.append(f"=== {host_clean} ===")
                ssl_results.extend(cert_lines)
                ssl_results.append("")
        except subprocess.TimeoutExpired:
            ssl_results.append(f"=== {host_clean} === [TIMEOUT]")
        except Exception as e:
            ssl_results.append(f"=== {host_clean} === [ERROR: {str(e)}]")

    save_output(output_dir, "ssl_certs.txt", "\n".join(ssl_results))
    log(output_dir, f"[dnsx] SSL cert info saved to ssl_certs.txt", "SUCCESS")

    mark_done(output_dir, MODULE)
