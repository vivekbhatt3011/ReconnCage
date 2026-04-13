#!/bin/bash

DOMAIN=$1

INPUT_FILE="output/subdomain_enum_output.txt"
OUTPUT_FILE="output/live_subdomains.txt"
LOG_FILE="output/recon.log"

echo "[+] Live Host Check Started for $DOMAIN" | tee -a $LOG_FILE

if [ ! -f "$INPUT_FILE" ]; then
    echo "[-] Input file not found: $INPUT_FILE" | tee -a $LOG_FILE
    exit 1
fi

echo "[+] Running HTTPX..." | tee -a $LOG_FILE

httpx -l $INPUT_FILE -silent -o $OUTPUT_FILE 2>>$LOG_FILE

if [ $? -eq 0 ]; then
    echo "[+] HTTPX completed successfully" | tee -a $LOG_FILE
else
    echo "[-] HTTPX failed" | tee -a $LOG_FILE
fi

echo "[+] Live Host Check Completed" | tee -a $LOG_FILE