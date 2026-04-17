#!/usr/bin/env python3

import sys
import concurrent.futures
from pathlib import Path

from utils import (
    banner, setup_output_dir, log, load_scope,
    verify_tools, PROFILES, CYAN, GREEN, YELLOW, RED, BOLD, NC
)

# ─── Modules ─────────────────────────────────
from modules import (
    whois_module,
    subfinder_module,
    httpx_module,
    dnsx_module,
    gau_module,
    whatweb_module,
    nmap_module,
    ffuf_module,
    dorking_module,
)

# ─── Tool Requirements per Profile ───────────
REQUIRED_TOOLS_BASE   = ["whois", "subfinder", "httpx", "dnsx", "gau", "nmap", "ffuf"]
REQUIRED_TOOLS_FULL   = REQUIRED_TOOLS_BASE + ["whatweb"]


def prompt_domain() -> str:
    print(f"{CYAN}{'─' * 50}{NC}")
    domain = input(f"{BOLD}  Enter target domain:{NC} ").strip()
    if not domain:
        print(f"{RED}[-] No domain provided. Exiting.{NC}")
        sys.exit(1)
    return domain


def prompt_profile() -> dict:
    print(f"\n{CYAN}{'─' * 50}{NC}")
    print(f"{BOLD}  Select profile:{NC}\n")
    print(f"  [1] Quick      (whois, subfinder, httpx, dnsx, gau, nmap, ffuf)")
    print(f"  [2] Standard   (whois, subfinder, httpx, dnsx, gau, whatweb, nmap, ffuf)")
    print(f"  [3] Deep       (whois, subfinder, httpx, dnsx, gau, whatweb, nmap, ffuf - recursive)")
    print(f"{CYAN}{'─' * 50}{NC}")
    choice = input(f"{BOLD}  Enter choice [1/2/3]:{NC} ").strip()
    if choice not in PROFILES:
        print(f"{RED}[-] Invalid choice. Defaulting to Standard.{NC}")
        choice = "2"
    profile = PROFILES[choice]
    print(f"\n{GREEN}[+] Profile selected: {profile['name']}{NC}\n")
    return profile


def run_pipeline(domain: str, profile: dict, output_dir: Path, scope: list):

    log(output_dir, f"ReconFlow started on {domain} | Profile: {profile['name']}")
    log(output_dir, f"Output directory: {output_dir}")

    # ── Phase 0: Whois (standalone) ──────────
    log(output_dir, "─── Phase 0: Whois ───────────────────────────")
    whois_module.run(domain, output_dir, profile, scope)

    # ── Phase 1: Subdomain Enumeration ───────
    log(output_dir, "─── Phase 1: Subdomain Enumeration ──────────")
    subdomains = subfinder_module.run(domain, output_dir, profile, scope)

    # ── Phase 2: Live Host Filtering ─────────
    log(output_dir, "─── Phase 2: Live Host Filtering ─────────────")
    live_hosts, dead_hosts = httpx_module.run(domain, output_dir, profile, scope, subdomains)

    if not live_hosts:
        log(output_dir, "No live hosts found. Continuing with limited recon.", "WARNING")

    # ── Phase 3: Parallel — dnsx + gau + whatweb ─
    log(output_dir, "─── Phase 3: DNS / GAU / WhatWeb (parallel) ──")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []

        futures.append(executor.submit(
            dnsx_module.run, domain, output_dir, profile, scope, live_hosts
        ))

        futures.append(executor.submit(
            gau_module.run, domain, output_dir, profile, scope
        ))

        if "whatweb" in profile["tools"]:
            futures.append(executor.submit(
                whatweb_module.run, domain, output_dir, profile, scope, live_hosts
            ))

        for f in concurrent.futures.as_completed(futures):
            try:
                f.result()
            except Exception as e:
                log(output_dir, f"Parallel phase error: {str(e)}", "ERROR")

    # ── Phase 4: Nmap Phase 1 ────────────────
    log(output_dir, "─── Phase 4: Nmap Phase 1 (surface scan) ─────")
    open_ports = nmap_module.run_phase1(domain, output_dir, profile, scope, live_hosts)

    # ── Phase 5: Nmap Phase 2 ────────────────
    log(output_dir, "─── Phase 5: Nmap Phase 2 (deep scan) ────────")
    nmap_module.run_phase2(domain, output_dir, profile, scope, live_hosts, open_ports)

    # ── Phase 6: Parallel — ffuf + dorking ───
    log(output_dir, "─── Phase 6: ffuf + Dorking (parallel) ───────")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = []

        futures.append(executor.submit(
            ffuf_module.run, domain, output_dir, profile, scope, live_hosts
        ))

        futures.append(executor.submit(
            dorking_module.run, domain, output_dir, profile, scope
        ))

        for f in concurrent.futures.as_completed(futures):
            try:
                f.result()
            except Exception as e:
                log(output_dir, f"Parallel phase error: {str(e)}", "ERROR")

    # ── Done ─────────────────────────────────
    log(output_dir, "─────────────────────────────────────────────")
    log(output_dir, f"ReconFlow completed on {domain}", "SUCCESS")
    log(output_dir, f"All outputs saved in: {output_dir}", "SUCCESS")
    print(f"\n{GREEN}{BOLD}  [+] Scan complete. Results saved to: {output_dir}{NC}\n")


def main():
    banner()

    domain  = prompt_domain()
    profile = prompt_profile()

    # Tool verification
    required = REQUIRED_TOOLS_FULL if "whatweb" in profile["tools"] else REQUIRED_TOOLS_BASE
    if not verify_tools(required):
        sys.exit(1)

    # Load scope
    scope = load_scope("scope.txt")
    if scope:
        print(f"{YELLOW}[*] Scope loaded: {len(scope)} entries from scope.txt{NC}")
    else:
        print(f"{YELLOW}[*] No scope.txt found. Running without scope filtering.{NC}")

    # Setup output directory
    output_dir = setup_output_dir(domain)
    print(f"{CYAN}[*] Output directory: {output_dir}{NC}\n")

    # Run
    run_pipeline(domain, profile, output_dir, scope)


if __name__ == "__main__":
    main()
