# ReconFlow

A modular recon automation framework for authorized penetration testing and bug bounty engagements.

---

## Setup

### 1. Install required tools
```bash
chmod +x requirements.sh
./requirements.sh
```

### 2. Add your wordlist
Place `big.txt` (or any wordlist) inside the `wordlists/` directory:
```
wordlists/big.txt
```

### 3. (Optional) Define scope
Create a `scope.txt` in the directory where you run the framework.
Any subdomain or host not matching an entry in this file will be filtered out.
```
# scope.txt example
targetdomain.com
sub.targetdomain.com
```
If no `scope.txt` is present, the framework runs without scope filtering.

---

## Usage

```bash
python3 main.py
```

You will be prompted to:
1. Enter the target domain
2. Select a scan profile

---

## Profiles

| Profile  | Tools                                          | Nmap P1        | Nmap P2         | ffuf Threads |
|----------|------------------------------------------------|----------------|-----------------|--------------|
| Quick    | whois, subfinder, httpx, dnsx, gau, nmap, ffuf | all ports -p-  | -sV             | 50           |
| Standard | + whatweb                                      | all ports -p-  | -sV -sC         | 100          |
| Deep     | + whatweb, recursive ffuf (depth 3)            | all ports -p-  | -sV -sC -A      | 150          |

---

## Output Structure

Each scan creates a folder in the current directory:
```
domainname_YYYY-MM-DD/
├── whois.txt
├── subdomains.txt
├── subdomains_raw.txt
├── live_hosts.txt
├── dead_hosts.txt
├── httpx_results.json
├── dnsx_results.txt
├── ssl_certs.txt
├── gau_urls.txt
├── whatweb_results.txt
├── nmap_phase1.txt
├── nmap_phase2.txt
├── ffuf/
│   └── <host>.txt  (one file per host)
├── dorks.txt
├── master.log
└── progress.json
```

---

## Checkpoint / Resume

If a scan is interrupted, re-run the same command with the same domain on the same date.
Completed modules will be skipped automatically based on `progress.json`.

---

## Tools Used

- [subfinder](https://github.com/projectdiscovery/subfinder)
- [httpx](https://github.com/projectdiscovery/httpx)
- [dnsx](https://github.com/projectdiscovery/dnsx)
- [gau](https://github.com/lc/gau)
- [ffuf](https://github.com/ffuf/ffuf)
- [nmap](https://nmap.org/)
- [whois](https://linux.die.net/man/1/whois)
- [whatweb](https://github.com/urbanadventurer/WhatWeb)

All tools are open source. No API keys required.

---

## Disclaimer

This tool is intended for authorized security testing only.
Always obtain written permission before scanning any target.
