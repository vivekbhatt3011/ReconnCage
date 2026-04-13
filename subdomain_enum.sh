#!/bin/bash

# Define output log file
LOG_FILE="logs/subdomain_enum.log"

# Define output file
OUTPUT_FILE="output/subdomain_enum_output.txt"

# Start logging
echo "Starting subdomain enumeration..." | tee -a $LOG_FILE

# Run Subfinder
echo "Running Subfinder..." | tee -a $LOG_FILE
subfinder -d example.com -o $OUTPUT_FILE 2>>$LOG_FILE

# Run Amass
echo "Running Amass..." | tee -a $LOG_FILE
amass enum -d example.com -o $OUTPUT_FILE 2>>$LOG_FILE

# Completion message
echo "Subdomain enumeration completed." | tee -a $LOG_FILE