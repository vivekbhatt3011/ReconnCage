#!/bin/bash

DOMAIN=$1

INPUT_FILE="output/live_subdomains.txt"
OUTPUT_FILE="output/waybackurls_output.txt"
LOG_FILE="output/recon.log"
TEMP_FILE="output/.wayback_tmp.txt"

echo "[+] Wayback URL Extraction Started for $DOMAIN" | tee -a $LOG_FILE

# Validation
if [ ! -f "$INPUT_FILE" ] || [ ! -s "$INPUT_FILE" ]; then
    echo "[-] Live subdomain file missing or empty" | tee -a $LOG_FILE
    exit 1
fi

echo "[+] Running waybackurls..." | tee -a $LOG_FILE

cat $INPUT_FILE | \
    waybackurls 2>>$LOG_FILE | \
    sed 's/:80//g;s/:443//g' | \
    sort -u > $TEMP_FILE

if [ ! -s "$TEMP_FILE" ]; then
    echo "[-] No URLs found" | tee -a $LOG_FILE
    rm -f $TEMP_FILE
    exit 1
fi

mv $TEMP_FILE $OUTPUT_FILE

echo "[+] Wayback URL Extraction Completed" | tee -a $LOG_FILE
echo "[+] Output: $OUTPUT_FILE" | tee -a $LOG_FILE