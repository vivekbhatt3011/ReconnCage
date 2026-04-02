# ReconCage 🔥

**ReconCage** is a modular reconnaissance framework designed to automate and enhance attack surface mapping for penetration testers.
It combines passive and active recon techniques with an intelligence layer to prioritize targets and streamline workflows.

---

## 🚀 Features

* 🧩 Modular architecture (plug-and-play tool integration)
* 🔍 Passive + Active reconnaissance pipeline
* 🔗 Smart data pipelining (raw → refined → intelligence)
* 🧠 Context-based intelligence layer
* 🎯 Target scoring and prioritization engine
* 🛡️ WAF-aware execution (adaptive scan strategy)
* 📂 Structured output management

---

## 🧠 Workflow

ReconCage follows a real-world penetration testing methodology:

1. **Passive Recon**

   * Subdomain enumeration (Subfinder)
   * Historical URL discovery (Wayback)

2. **Active Recon**

   * Live host probing (HTTPX)
   * Port scanning (Nmap)
   * Vulnerability scanning (Nuclei)
   * Endpoint fuzzing (FFUF)

3. **Pipeline Processing**

   * Subdomains → Alive hosts
   * URLs → Fuzzing inputs
   * Ports → Targeted scans

4. **Intelligence Layer**

   * Context aggregation
   * Tech stack detection
   * Target scoring & prioritization

---

## 🏗️ Project Structure

```
reconcage/
│
├── core/              # Framework logic
├── modules/           # Tool integrations
├── output/            # Scan results
│   ├── raw/
│   ├── refined/
│   └── intel/
│
└── main.py            # Entry point
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/reconcage.git
cd reconcage
```

### 2. Install required tools

Make sure the following tools are installed and available in PATH:

* subfinder
* httpx
* nuclei
* ffuf
* nmap
* wafw00f
* waybackurls

(Optional)

* gowitness
* sslscan

---

## ▶️ Usage

```bash
python main.py
```

Enter the target domain when prompted.

---

## 📂 Output Structure

```
target.com/
│
├── raw/        # Full tool outputs
├── refined/    # Processed pipeline data
├── intel/      # Scoring & intelligence
│
├── interesting.txt   # Key findings
└── target.com.txt    # Master log
```

---

## 🎯 Use Cases

* Bug bounty reconnaissance
* Attack surface mapping
* Web application testing
* Red team initial access recon

---

## ⚠️ Disclaimer

This tool is intended for **educational purposes and authorized security testing only**.
Do not use it against systems without proper permission.

---

## 👨‍💻 Author

Built by a penetration tester focused on offensive security, automation, and real-world attack workflows.

---
