from datetime import datetime

def log(msg):
    print(f"[{datetime.now():%H:%M:%S}] {msg}")
