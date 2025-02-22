#!/bin/bash

FILE="Sample.txt"
LOGFILE="file_log.log"
LAST_HASH="last_hash.txt"

# Compute file hash
NEW_HASH=$(md5sum "$FILE" | awk '{print $1}')

# Compare with last hash
if [ -f "$LAST_HASH" ]; then
    OLD_HASH=$(cat "$LAST_HASH")
    if [ "$NEW_HASH" != "$OLD_HASH" ]; then
        echo "$(date): $FILE changed!" >> "$LOGFILE"
        echo "$NEW_HASH" > "$LAST_HASH"
    fi
else
    echo "$NEW_HASH" > "$LAST_HASH"
fi
