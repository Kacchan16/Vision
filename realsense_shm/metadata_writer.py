from multiprocessing.shared_memory import SharedMemory
import numpy as np
import struct

class MetadataWriter:

    def __init__(self, name):
        MAX_METADATA_SIZE = 1024
        self.HEADER_SIZE = 4
        self.shm = SharedMemory(
            name=name,
            create=True,
            size=self.HEADER_SIZE + MAX_METADATA_SIZE
        )
    
    def write(self,metadata_bytes):
        #metadata_shm.buf[:len(metadata_bytes)] = metadata_bytes
        size = len(metadata_bytes)
        if size > 1024:
            raise ValueError("Metadata exceeds shared memory capacity")
        else:
            self.shm.buf[:self.HEADER_SIZE] = struct.pack("I",size)
            self.shm.buf[self.HEADER_SIZE: self.HEADER_SIZE+size] = metadata_bytes

    def close(self):
        self.shm.close()

    def unlink(self):
        self.shm.unlink()
