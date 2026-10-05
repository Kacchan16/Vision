from multiprocessing.shared_memory import SharedMemory
import numpy as np


class MetadataWriter:

    def __init__(self, name):

        self.dtype = np.dtype([
            ("frame_id", np.uint64),
            ("timestamp", np.float64),
            ("width", np.uint32),
            ("height", np.uint32)
        ])

        self.shm = SharedMemory(
            name=name,
            create=True,
            size=self.dtype.itemsize
        )

        self.data = np.ndarray(
            (1,),
            dtype=self.dtype,
            buffer=self.shm.buf
        )

    def update(
    self,
    frame_id,
    timestamp,
    width,
    height
):

        self.data[0]["frame_id"] = frame_id
        self.data[0]["timestamp"] = timestamp
        self.data[0]["width"] = width
        self.data[0]["height"] = height