import time
import sys
from datetime import datetime

print("Codespace keep-alive script started. Press Ctrl+C to stop.")

try:
    while True:
        # Get the current time stamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Keep-alive pulse sent at: {current_time}")
        
        # Force Python to push the output to the terminal immediately
        sys.stdout.flush() 
        
        # Wait for 60 seconds
        time.sleep(60)
except KeyboardInterrupt:
    print("\nKeep-alive script stopped successfully.")
