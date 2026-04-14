#!/bin/bash

DOMAIN=$1

OUTPUT_FILE="output/github_dorks.txt"
LOG_FILE="output/recon.log"
TEMP_FILE="output/.github_tmp.txt"

echo "[+] GitHub Dorking Started for $DOMAIN" | tee -a $LOG_FILE

# Validation
if [ -z "$DOMAIN" ]; then
    echo "[-] No domain provided" | tee -a $LOG_FILE
    exit 1
fi

echo "[+] Running GitHub dorks (via gitdorker patterns)..." | tee -a $LOG_FILE

# Basic dorks (no API required)
DORKS=(
    "$DOMAIN password"
    "$DOMAIN api_key"
    "$DOMAIN secret"
    "$DOMAIN token"
    "$DOMAIN config"
    "$DOMAIN db_password"
    "$DOMAIN authorization"
)

> $TEMP_FILE

# Loop through dorks
for dork in "${DORKS[@]}"; do
    echo "[+] Searching: $dork" | tee -a $LOG_FILE

    curl -s "https://github.com/search?q=$dork&type=code" \
    | grep -Eo 'href="/[^"]+"' \
    | grep "$DOMAIN" \
    | sed 's/href="//;s/"$//' \
    | sort -u >> $TEMP_FILE

done

# Validation
if [ ! -s "$TEMP_FILE" ]; then
    echo "[-] No GitHub results found" | tee -a $LOG_FILE
    rm -f $TEMP_FILE
    exit 1
fi

sort -u $TEMP_FILE > $OUTPUT_FILE
rm -f $TEMP_FILE

echo "[+] GitHub Dorking Completed" | tee -a $LOG_FILE
echo "[+] Output: $OUTPUT_FILE" | tee -a $LOG_FILE