#!/bin/bash

DOMAIN=$1

INPUT_FILE="output/live_subdomains.txt"
OUTPUT_FILE="output/gau_output.txt"
LOG_FILE="output/recon.log"
TEMP_FILE="output/.gau_tmp.txt"

echo "[+] GAU URL Collection Started for $DOMAIN" | tee -a $LOG_FILE

# Validation
if [ ! -f "$INPUT_FILE" ] || [ ! -s "$INPUT_FILE" ]; then
    echo "[-] Live subdomain file missing or empty" | tee -a $LOG_FILE
    exit 1
fi

echo "[+] Running GAU (multi-source collection)..." | tee -a $LOG_FILE

cat $INPUT_FILE | \
    gau --threads 5 \
        --subs \
        --blacklist png,jpg,jpeg,gif,svg,css,woff,woff2,ttf \
        2>>$LOG_FILE | \
    sed 's/:80//g;s/:443//g' | \
    sort -u > $TEMP_FILE

# Validation
if [ ! -s "$TEMP_FILE" ]; then
    echo "[-] GAU returned no results" | tee -a $LOG_FILE
    rm -f $TEMP_FILE
    exit 1
fi

mv $TEMP_FILE $OUTPUT_FILE

echo "[+] GAU Collection Completed" | tee -a $LOG_FILE
echo "[+] Output: $OUTPUT_FILE" | tee -a $LOG_FILE