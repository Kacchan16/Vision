from multiprocessing.shared_memory import SharedMemory
import numpy as np

class SharedMemoryWriter:
    def __init__(self, name, shape, dtype):
        self.name = name
        self.shape = shape
        self.dtype = dtype
        self.frame_id = 0
        size = np.zeros(shape, dtype=dtype).nbytes
        self.shm = SharedMemory(name=name, create=True, size=size)
        self.array = np.ndarray(shape= shape,
                                dtype=dtype, buffer=self.shm.buf)
        
    def write(self, image):
        self.array[:] = image
        self.frame_id += 1


    def close(self):
        self.shm.close()
    
    def unlink(self):
        self.shm.unlink()

    #writer.write(image)
