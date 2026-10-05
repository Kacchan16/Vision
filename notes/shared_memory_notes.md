shared memory

it knows only bytes, no images.
shm.buf - memoryview

shm.buf[:] = color_image.tobytes()

color = np.ndarray(
    (480,640,3),
    dtype=np.uint8,
    buffer=shm.buf
)

no encoding, share just raw pixel bytes.

shm = SharedMemory(name="testing",create=True, size=100)

only one process creates it, everyone attaches to it. SharedMemory(name="camera", create=False)

writer class - create memory, write image, close.

reader class - attach, return numpy array, close.

2 memory block - color_shm, depth_shm
compute exact sizes and use dtype, shape for each.

metadata - add flatbuffers
send only metadata-

Camera
      ↓
Shared Memory
      ↓
Metadata

Shared Memory
      ↓
NumPy
      ↓
YOLO


