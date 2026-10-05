from multiprocessing.shared_memory import SharedMemory
import numpy as np


class MetadataReader:

    def __init__(self,name):

        dtype = np.dtype([
            ("frame_id", np.uint64),
            ("timestamp", np.float64),
            ("width", np.uint32),
            ("height", np.uint32)
        ])


        self.shm = SharedMemory(
            name=name,
            create=False
        )


        self.data = np.ndarray(
            (1,),
            dtype=dtype,
            buffer=self.shm.buf
        )


    def read(self):
        return self.data[0]