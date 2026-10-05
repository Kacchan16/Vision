import time

from multiprocessing.shared_memory import SharedMemory

shm = SharedMemory(name="camera_test", create=False)

data = list(shm.buf[:4])

print(data)

shm.close()