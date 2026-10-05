
# Write a few bytes into shm.buf (for example the values 1, 2, 3, 4).
# Read those same bytes back and print them.
# Close and unlink the shared memory.

from multiprocessing.shared_memory import SharedMemory

shm = SharedMemory(name="testing",create=True, size=100)
print(shm.name)
print(shm.size)
#print(dir(shm.buf))
jj=bytes([2,3,4,5])
shm.buf[:4] = jj
print(type(shm.buf))
print(len(shm.buf))
print(list(shm.buf[:10]))
shm.close()
shm.unlink()