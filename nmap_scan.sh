#!/bin/bash

DOMAIN=$1

INPUT_FILE="output/live_subdomains.txt"
FAST_OUTPUT="output/nmap_fast.txt"
DETAIL_OUTPUT="output/nmap_detailed.txt"
LOG_FILE="output/recon.log"
PORTS_FILE="output/.ports_tmp.txt"

echo "[+] Nmap Scan Started for $DOMAIN" | tee -a $LOG_FILE

# Validation
if [ ! -f "$INPUT_FILE" ] || [ ! -s "$INPUT_FILE" ]; then
    echo "[-] Live subdomain file missing or empty" | tee -a $LOG_FILE
    exit 1
fi

echo "[+] Phase 1: Fast Port Scan Started..." | tee -a $LOG_FILE

> $FAST_OUTPUT
> $PORTS_FILE

# Loop through hosts (linear execution as per your design)
while read host; do
    echo "[+] Scanning (fast): $host" | tee -a $LOG_FILE
    
    nmap -p- \
         --min-rate 1000 \
         -T4 \
         --open \
         -oN - $host 2>>$LOG_FILE | tee -a $FAST_OUTPUT

done < $INPUT_FILE

echo "[+] Fast Scan Completed" | tee -a $LOG_FILE

# Extract open ports
echo "[+] Extracting open ports..." | tee -a $LOG_FILE

grep "Ports:" $FAST_OUTPUT | \
grep -oP '\d+/open' | \
cut -d'/' -f1 | \
sort -u | tr '\n' ',' | sed 's/,$//' > $PORTS_FILE

if [ ! -s "$PORTS_FILE" ]; then
    echo "[-] No open ports found" | tee -a $LOG_FILE
    exit 1
fi

PORTS=$(cat $PORTS_FILE)

echo "[+] Open ports identified: $PORTS" | tee -a $LOG_FILE

echo "[+] Phase 2: Detailed Scan Started..." | tee -a $LOG_FILE

> $DETAIL_OUTPUT

while read host; do
    echo "[+] Scanning (detailed): $host" | tee -a $LOG_FILE

    nmap -p $PORTS \
         -sC \
         -sV \
         -T3 \
         --open \
         -oN - $host 2>>$LOG_FILE | tee -a $DETAIL_OUTPUT

done < $INPUT_FILE

echo "[+] Detailed Scan Completed" | tee -a $LOG_FILE
echo "[+] Output: $DETAIL_OUTPUT" | tee -a $LOG_FILE

echo "[+] Nmap Scan Completed" | tee -a $LOG_FILE