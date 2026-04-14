#!/bin/bash

DOMAIN=$1

INPUT_FILE="output/subdomains.txt"
OUTPUT_FILE="output/live_subdomains.txt"
LOG_FILE="output/recon.log"
TEMP_FILE="output/.httpx_tmp.txt"

echo "[+] Live Host Check Started for $DOMAIN" | tee -a $LOG_FILE

# Validation
if [ ! -f "$INPUT_FILE" ] || [ ! -s "$INPUT_FILE" ]; then
    echo "[-] Subdomain file missing or empty" | tee -a $LOG_FILE
    exit 1
fi

echo "[+] Running HTTPX (accurate probing)..." | tee -a $LOG_FILE

httpx -l $INPUT_FILE \
      -silent \
      -follow-redirects \
      -status-code \
      -title \
      -tech-detect \
      -timeout 10 \
      -retries 2 \
      2>>$LOG_FILE > $TEMP_FILE

# Extract only live URLs (first column)
awk '{print $1}' $TEMP_FILE | sort -u > $OUTPUT_FILE

if [ ! -s "$OUTPUT_FILE" ]; then
    echo "[-] No live hosts found" | tee -a $LOG_FILE
    rm -f $TEMP_FILE
    exit 1
fi

rm -f $TEMP_FILE

echo "[+] Live Host Check Completed" | tee -a $LOG_FILE
echo "[+] Output: $OUTPUT_FILE" | tee -a $LOG_FILE