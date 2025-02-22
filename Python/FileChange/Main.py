import time
import shutil
import os
from datetime import datetime

SOURCE_FILE = "Demo.txt"  
BACKUP_FILE = "BackUp.txt"     
LOG_FILE = "backup_log.txt"
BACKUP_INTERVAL = 2  

last_modified = os.path.getmtime(SOURCE_FILE)

def log_backup(message):
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now()} - {message}\n")

print("Monitoring file for changes...")
log_backup("Backup script started.")

while True:
    time.sleep(BACKUP_INTERVAL)
    
    current_modified = os.path.getmtime(SOURCE_FILE)
    if current_modified != last_modified:
        shutil.copy(SOURCE_FILE, BACKUP_FILE)
        
        print(f"Backup updated: {BACKUP_FILE}")
        log_backup(f"Backup updated: {BACKUP_FILE}")
        
        last_modified = current_modified
