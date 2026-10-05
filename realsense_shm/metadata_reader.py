from multiprocessing.shared_memory import SharedMemory
import numpy as np
import struct


class MetadataReader:

    def __init__(self,name):

        self.shm = SharedMemory(
            name=name,
            create=False
        )

    def read(self):
        
        size = struct.unpack(
                        "I",
                    self.shm.buf[:4]
                    )[0]
        if size <= 0 or size > 1024:
            raise ValueError("Invalid metadata size")
        else:
            data = self.shm.buf[4:4+size]
            return bytes(data)

    def close(self):
        self.shm.close()