from multiprocessing.shared_memory import SharedMemory
import numpy as np


class SharedMemoryReader:

    def __init__(self, name, shape, dtype):

        self.name = name
        self.shape = shape
        self.dtype = dtype

        self.shm = SharedMemory(
            name=name,
            create=False
        )

        self.array = np.ndarray(
            shape,
            dtype=dtype,
            buffer=self.shm.buf
        )
    
    def read(self):
        return self.array
    
    def close(self):
        self.shm.close()
    #image = reader.read()