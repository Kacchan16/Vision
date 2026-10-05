import time
from multiprocessing.shared_memory import SharedMemory


shm = SharedMemory(
    name="camera_test",
    create=True,
    size=100
)

shm.buf[:4] = bytes([10,20,30,40])

print("Writer running")
print(shm.name)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    shm.close()
    shm.unlink()