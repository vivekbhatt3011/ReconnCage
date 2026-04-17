import os
import json
import datetime
import subprocess
from pathlib import Path

# ─────────────────────────────────────────────
#  ReconFlow - Shared Utilities
# ─────────────────────────────────────────────

CYAN    = "\033[0;36m"
GREEN   = "\033[0;32m"
YELLOW  = "\033[1;33m"
RED     = "\033[0;31m"
BOLD    = "\033[1m"
NC      = "\033[0m"

def banner():
    print(f"{CYAN}")
    print("  ____                      _____ _")
    print(" |  _ \\ ___  ___ ___  _ __ |  ___| | _____      __")
    print(" | |_) / _ \\/ __/ _ \\| '_ \\| |_  | |/ _ \\ \\ /\\ / /")
    print(" |  _ <  __/ (_| (_) | | | |  _| | | (_) \\ V  V / ")
    print(" |_| \\_\\___|\\___\\___/|_| |_|_|   |_|\\___/ \\_/\\_/  ")
    print(f"{NC}")
    print(f"{YELLOW}  Recon Automation Framework{NC}\n")


def setup_output_dir(domain: str) -> Path:
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    folder_name = f"{domain}_{date_str}"
    output_dir = Path.cwd() / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def get_master_log(output_dir: Path) -> Path:
    return output_dir / "master.log"


def log(output_dir: Path, message: str, level: str = "INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    log_file = get_master_log(output_dir)
    with open(log_file, "a") as f:
        f.write(log_line + "\n")
    if level == "INFO":
        print(f"{CYAN}[*]{NC} {message}")
    elif level == "SUCCESS":
        print(f"{GREEN}[+]{NC} {message}")
    elif level == "WARNING":
        print(f"{YELLOW}[!]{NC} {message}")
    elif level == "ERROR":
        print(f"{RED}[-]{NC} {message}")


def load_scope(scope_file: str = "scope.txt") -> list:
    scope_path = Path(scope_file)
    if not scope_path.exists():
        return []
    with open(scope_path) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def filter_scope(items: list, scope: list) -> list:
    if not scope:
        return items
    filtered = []
    for item in items:
        for s in scope:
            if s in item:
                filtered.append(item)
                break
    return filtered


def save_output(output_dir: Path, filename: str, content: str):
    filepath = output_dir / filename
    with open(filepath, "w") as f:
        f.write(content)
    return filepath


def read_lines(filepath: Path) -> list:
    if not filepath.exists():
        return []
    with open(filepath) as f:
        return [line.strip() for line in f if line.strip()]


def check_tool(tool_name: str) -> bool:
    result = subprocess.run(["which", tool_name], capture_output=True, text=True)
    return result.returncode == 0


def verify_tools(required_tools: list) -> bool:
    missing = []
    for tool in required_tools:
        if not check_tool(tool):
            missing.append(tool)
    if missing:
        for t in missing:
            print(f"{RED}[-] Tool '{t}' not found. Please run requirements.sh first.{NC}")
        return False
    return True


# ─── Checkpoint / Resume ─────────────────────

def load_progress(output_dir: Path) -> dict:
    progress_file = output_dir / "progress.json"
    if progress_file.exists():
        with open(progress_file) as f:
            return json.load(f)
    return {}


def mark_done(output_dir: Path, module: str):
    progress = load_progress(output_dir)
    progress[module] = "done"
    progress_file = output_dir / "progress.json"
    with open(progress_file, "w") as f:
        json.dump(progress, f, indent=2)


def is_done(output_dir: Path, module: str) -> bool:
    progress = load_progress(output_dir)
    return progress.get(module) == "done"


# ─── Profile Definitions ─────────────────────

PROFILES = {
    "1": {
        "name": "Quick",
        "tools": ["whois", "subfinder", "httpx", "dnsx", "gau", "nmap", "ffuf"],
        "nmap_phase1_flags": "-T4 -p-",
        "nmap_phase2_flags": "-T4 -sV",
        "ffuf_threads": 50,
        "ffuf_recursive_depth": 0,
    },
    "2": {
        "name": "Standard",
        "tools": ["whois", "subfinder", "httpx", "dnsx", "gau", "whatweb", "nmap", "ffuf"],
        "nmap_phase1_flags": "-T4 -p-",
        "nmap_phase2_flags": "-T4 -sV -sC",
        "ffuf_threads": 100,
        "ffuf_recursive_depth": 0,
    },
    "3": {
        "name": "Deep",
        "tools": ["whois", "subfinder", "httpx", "dnsx", "gau", "whatweb", "nmap", "ffuf"],
        "nmap_phase1_flags": "-T4 -p-",
        "nmap_phase2_flags": "-T4 -sV -sC -A",
        "ffuf_threads": 150,
        "ffuf_recursive_depth": 3,
    },
}
