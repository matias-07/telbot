from datetime import datetime

def log(message, newline=False):
    """Logs a message to the console.
    If newline is True, logs the message followed
    by a newline character (\n).
    """
    now = str(datetime.now())[:-7]
    if newline: print()
    print(f"[{now}] {message}")
