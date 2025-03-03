#!/bin/bash

LOG_FILE="system_performance.log"
MAX_LINES=100

echo "System Performance Monitoring Started: $(date)" >> $LOG_FILE

while true; do
    echo "--------------------" >> $LOG_FILE
    echo "Date & Time: $(date)" >> $LOG_FILE

    # CPU Usage
    echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')%" >> $LOG_FILE

    # RAM Usage
    echo "RAM Usage: $(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')" >> $LOG_FILE

    # Disk Usage
    echo "Disk Usage: $(df -h / | awk 'NR==2 {print $5}')" >> $LOG_FILE

    # Network Usage
    RX=$(cat /sys/class/net/eth0/statistics/rx_bytes)
    TX=$(cat /sys/class/net/eth0/statistics/tx_bytes)
    echo "Network Usage: RX ${RX} bytes, TX ${TX} bytes" >> $LOG_FILE

    # Ensure file has at most MAX_LINES lines (delete oldest if needed)
    if [ $(wc -l < "$LOG_FILE") -gt $MAX_LINES ]; then
        sed -i '1d' "$LOG_FILE"  # Delete first (oldest) line
    fi

    sleep 60  # Log every minute
done
