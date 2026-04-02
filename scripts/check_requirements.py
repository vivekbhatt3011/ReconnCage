import shutil


REQUIRED_TOOLS = [
    "subfinder",
    "waybackurls",
    "httpx",
    "nuclei",
    "ffuf",
    "nmap",
    "wafw00f",
    "curl"
]


def check_tools():
    """
    Check if required tools exist in system PATH.
    """

    print("\n[+] Checking required tools...\n")

    missing_tools = []

    for tool in REQUIRED_TOOLS:
        if shutil.which(tool):
            print(f"[OK] {tool}")
        else:
            print(f"[MISSING] {tool}")
            missing_tools.append(tool)

    print("\n-----------------------------\n")

    if missing_tools:
        print("[!] Missing tools detected:\n")
        for tool in missing_tools:
            print(f" - {tool}")

        print("\n[!] Install missing tools before running ReconCage.\n")
        return False

    print("[+] All tools are installed.\n")
    return True


if __name__ == "__main__":
    check_tools()