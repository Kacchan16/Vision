import numpy as np

from realsense_shm.writer import SharedMemoryWriter
from realsense_shm.reader import SharedMemoryReader


shape = (480,640,3)


writer = SharedMemoryWriter(
    "color_camera",
    shape,
    np.uint8
)


image = np.ones(shape, dtype=np.uint8) * 50

writer.write(image)


reader = SharedMemoryReader(
    "color_camera",
    shape,
    np.uint8
)


received = reader.read()

print(received.shape)
print(received[0,0])


reader.close()
writer.close()