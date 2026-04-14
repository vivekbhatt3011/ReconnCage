#!/bin/bash

DOMAIN=$1

INPUT_FILE="output/waybackurls_output.txt"
LOG_FILE="output/recon.log"

PARAMS_ALL="output/params_all.txt"
PARAMS_XSS="output/params_xss.txt"
PARAMS_SQLI="output/params_sqli.txt"
PARAMS_SSRF="output/params_ssrf.txt"
PARAMS_LFI="output/params_lfi.txt"

TEMP_FILE="output/.params_tmp.txt"

echo "[+] GF Parameter Extraction Started for $DOMAIN" | tee -a $LOG_FILE

# Validation
if [ ! -f "$INPUT_FILE" ] || [ ! -s "$INPUT_FILE" ]; then
    echo "[-] Wayback URL file missing or empty" | tee -a $LOG_FILE
    exit 1
fi

echo "[+] Extracting parameterized URLs..." | tee -a $LOG_FILE

# Extract only URLs with parameters
grep "=" "$INPUT_FILE" | sort -u > $TEMP_FILE

if [ ! -s "$TEMP_FILE" ]; then
    echo "[-] No parameterized URLs found" | tee -a $LOG_FILE
    rm -f $TEMP_FILE
    exit 1
fi

mv $TEMP_FILE $PARAMS_ALL

echo "[+] Total parameterized URLs saved: $PARAMS_ALL" | tee -a $LOG_FILE

# GF Filtering
echo "[+] Running GF patterns..." | tee -a $LOG_FILE

gf xss $PARAMS_ALL | sort -u > $PARAMS_XSS 2>>$LOG_FILE
gf sqli $PARAMS_ALL | sort -u > $PARAMS_SQLI 2>>$LOG_FILE
gf ssrf $PARAMS_ALL | sort -u > $PARAMS_SSRF 2>>$LOG_FILE
gf lfi $PARAMS_ALL | sort -u > $PARAMS_LFI 2>>$LOG_FILE

echo "[+] GF Filtering Completed" | tee -a $LOG_FILE

echo "[+] Outputs:"
echo "    - All Params: $PARAMS_ALL" | tee -a $LOG_FILE
echo "    - XSS:        $PARAMS_XSS" | tee -a $LOG_FILE
echo "    - SQLi:       $PARAMS_SQLI" | tee -a $LOG_FILE
echo "    - SSRF:       $PARAMS_SSRF" | tee -a $LOG_FILE
echo "    - LFI:        $PARAMS_LFI" | tee -a $LOG_FILE

echo "[+] GF Parameter Extraction Completed" | tee -a $LOG_FILE