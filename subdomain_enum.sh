#!/bin/bash

DOMAIN=$1

OUTPUT_DIR="output"
LOG_FILE="$OUTPUT_DIR/recon.log"
SUBDOMAIN_FILE="$OUTPUT_DIR/subdomains.txt"
TEMP_FILE="$OUTPUT_DIR/.sub_tmp.txt"

echo "[+] Subdomain Enumeration Started for $DOMAIN" | tee -a $LOG_FILE

# Validation
if [ -z "$DOMAIN" ]; then
    echo "[-] No domain provided" | tee -a $LOG_FILE
    exit 1
fi

echo "[+] Running Subfinder..." | tee -a $LOG_FILE
subfinder -d $DOMAIN -all -recursive -silent 2>>$LOG_FILE > $TEMP_FILE

echo "[+] Running Amass (passive)..." | tee -a $LOG_FILE
amass enum -passive -d $DOMAIN 2>>$LOG_FILE >> $TEMP_FILE

# Validation
if [ ! -s "$TEMP_FILE" ]; then
    echo "[-] No subdomains found" | tee -a $LOG_FILE
    rm -f $TEMP_FILE
    exit 1
fi

# Deduplicate
sort -u $TEMP_FILE > $SUBDOMAIN_FILE
rm -f $TEMP_FILE

echo "[+] Subdomain Enumeration Completed" | tee -a $LOG_FILE
echo "[+] Output: $SUBDOMAIN_FILE" | tee -a $LOG_FILE