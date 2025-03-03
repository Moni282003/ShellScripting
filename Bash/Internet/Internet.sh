#!/bin/bash

LOG_FILE="internet_speed.log"
THRESHOLD=5  # Set your speed threshold in Mbps

while true; do
    SPEED=$(speedtest-cli --simple | grep "Download" | awk '{print $2}')

    if [[ -z "$SPEED" ]]; then
        echo "$(date) No internet connection!" | tee -a "$LOG_FILE"
        notify-send "Internet Alert" "No internet connection detected!"
    elif (( $(echo "$SPEED < $THRESHOLD" | bc -l) )); then
        echo "$(date) Slow Internet: $SPEED Mbps" | tee -a "$LOG_FILE"
        notify-send "Internet Alert" "Slow Internet: $SPEED Mbps"
    else
        echo "$(date) Internet OK: $SPEED Mbps" | tee -a "$LOG_FILE"
    fi

    sleep 10  # Check every 5 minutes
done
