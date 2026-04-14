#!/bin/bash

DOMAIN=$1

OUTPUT_FILE="output/google_dorks.txt"
LOG_FILE="output/recon.log"

echo "[+] Google Dorking Started for $DOMAIN" | tee -a $LOG_FILE

# Validation
if [ -z "$DOMAIN" ]; then
    echo "[-] No domain provided" | tee -a $LOG_FILE
    exit 1
fi

echo "[+] Generating high-value dorks..." | tee -a $LOG_FILE

cat <<EOF > $OUTPUT_FILE
site:$DOMAIN ext:env
site:$DOMAIN ext:sql
site:$DOMAIN ext:log
site:$DOMAIN ext:bak
site:$DOMAIN ext:zip
site:$DOMAIN ext:tar
site:$DOMAIN ext:gz

site:$DOMAIN inurl:admin
site:$DOMAIN inurl:login
site:$DOMAIN inurl:dashboard
site:$DOMAIN inurl:panel

site:$DOMAIN intitle:"index of"
site:$DOMAIN "Index of /"

site:$DOMAIN "password"
site:$DOMAIN "api_key"
site:$DOMAIN "secret"
site:$DOMAIN "token"

site:$DOMAIN inurl:config
site:$DOMAIN inurl:backup
site:$DOMAIN inurl:old
site:$DOMAIN inurl:test
site:$DOMAIN inurl:dev
EOF

if [ ! -s "$OUTPUT_FILE" ]; then
    echo "[-] Failed to generate dorks" | tee -a $LOG_FILE
    exit 1
fi

echo "[+] Google Dorks Generated Successfully" | tee -a $LOG_FILE
echo "[+] Output: $OUTPUT_FILE" | tee -a $LOG_FILE