#!/bin/bash

DOMAIN=$1

INPUT_FILE="output/live_subdomains.txt"
OUTPUT_FILE="output/whatweb_output.txt"
LOG_FILE="output/recon.log"
TEMP_FILE="output/.whatweb_tmp.txt"

echo "[+] WhatWeb Scan Started for $DOMAIN" | tee -a $LOG_FILE

# Validation
if [ ! -f "$INPUT_FILE" ] || [ ! -s "$INPUT_FILE" ]; then
    echo "[-] Live subdomain file missing or empty" | tee -a $LOG_FILE
    exit 1
fi

echo "[+] Running WhatWeb..." | tee -a $LOG_FILE

whatweb -i $INPUT_FILE \
        --aggression 3 \
        --level 3 \
        --no-errors \
        --log-verbose=$TEMP_FILE \
        2>>$LOG_FILE

if [ ! -s "$TEMP_FILE" ]; then
    echo "[-] WhatWeb returned no results" | tee -a $LOG_FILE
    rm -f $TEMP_FILE
    exit 1
fi

sed '/^$/d' $TEMP_FILE > $OUTPUT_FILE
rm -f $TEMP_FILE

echo "[+] WhatWeb Scan Completed" | tee -a $LOG_FILE
echo "[+] Output: $OUTPUT_FILE" | tee -a $LOG_FILE