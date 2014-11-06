import os
import time

SECONDS = 3

while True:
    initial = time.time()
    os.system("python manage.py update_status")
    end = time.time()
    total_time = end - initial
    remaining = SECONDS - total_time
    if remaining > 0:
        time.sleep(remaining)
