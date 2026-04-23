# ===== THREADING — concurrent I/O-bound tasks =====
import threading
import time
from threading import Lock, Event


# 1. Basic thread creation
def download_file(filename: str, delay: float) -> None:
    print(f"  Starting download: {filename}")
    time.sleep(delay)                        # simulate I/O wait
    print(f"  Finished download: {filename}")

files = [("report.pdf", 2), ("image.png", 1), ("data.csv", 1.5)]
threads = []

start = time.time()
for name, delay in files:
    t = threading.Thread(target=download_file, args=(name, delay))
    threads.append(t)
    t.start()

for t in threads:
    t.join()                                 # wait for all to finish

print(f"All downloads done in {time.time()-start:.2f}s") 