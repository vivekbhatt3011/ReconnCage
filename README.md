# Reconnaissance Framework

## Overview

This reconnaissance framework is designed for security professionals to systematically identify and assess potential security risks. It operates in a linear fashion, executing each tool sequentially.

## Features

* **Modular Design**: Separate scripts for different tasks like subdomain enumeration, URL extraction, web technology fingerprinting, live checks, port scanning, and dorking.
* **Detailed Logging**: Logs start and completion messages for each tool, providing clear tracking of the reconnaissance process.

## Tools Included

* **Subfinder & Amass**: Subdomain enumeration
* **Waybackurls**: Extract URLs from the Wayback Machine
* **WhatWeb**: Web technology fingerprinting
* **HTTPX/Curl**: Live checks to see if hosts are alive
* **Nmap**: Port scanning
* **GitHub Dorking**: Search for information on GitHub using dorks
* **Google Dorking**: Search for information using Google search queries

## Installation

1. **Install Required Tools**: Ensure you have `Subfinder`, `Amass`, `Waybackurls`, `WhatWeb`, `HTTPX`, `Curl`, `Nmap`, and dorking tools installed.
2. **Clone Repository**: Clone this repository to your local machine.
3. **Run Scripts**: Execute the scripts in the desired sequence.

## Usage

* Run `subdomain_enum.sh` for subdomain enumeration.
* Run `waybackurls.sh` to extract URLs.
* Run `whatweb.sh` for web technology fingerprinting.
* Run `httpx_check.sh` for live checks.
* Run `nmap_scan.sh` for port scanning.
* Run `github_dorking.sh` and `google_dorking.sh` for dorking on GitHub and Google.
