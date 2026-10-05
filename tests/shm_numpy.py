from multiprocessing.shared_memory import SharedMemory
import numpy as np

shape = (480, 640, 3)

size = np.zeros(shape, dtype=np.uint8).nbytes

print(size)

shm = SharedMemory(name="numpy_test", create=True, size=size)

image=np.ndarray(shape, dtype=np.uint8, buffer=shm.buf)

image[:]=100

print(image.shape)
print(image[0,0])


shm.close()
shm.unlink()