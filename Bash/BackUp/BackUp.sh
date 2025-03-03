#!/bin/bash

SOURCE_FILE="source.txt"
BACKUP_FILE="backup.txt"
LOG_FILE="backup.log"

# Ensure the backup and log files exist
touch "$BACKUP_FILE" "$LOG_FILE"

echo "Monitoring changes in '$SOURCE_FILE'... Press Ctrl+C to stop."

# Infinite loop to check for changes
while true; do
    # Wait for modification in the source file
    inotifywait -e modify "$SOURCE_FILE" > /dev/null 2>&1
    
    # Copy the updated content to the backup file
    cp "$SOURCE_FILE" "$BACKUP_FILE"
    
    # Log only when changes occur
    echo "$(date): Backup updated." >> "$LOG_FILE"
done
