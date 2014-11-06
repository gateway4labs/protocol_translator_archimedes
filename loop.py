import os
import sys
import time

SECONDS = 3

FAKE = len(sys.argv) > 1 and sys.argv[1] == '--fake'

while True:
    initial = time.time()
    if FAKE:
        os.system("python manage.py update_status --fake")
    else:
        os.system("python manage.py update_status --fake")
    end = time.time()
    total_time = end - initial
    remaining = SECONDS - total_time
    if remaining > 0:
        time.sleep(remaining)
