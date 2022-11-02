from reader import ReaderProcess, AbstractEngine, EngineType
import numpy as np


class SharedMemory():
	def __init__(self):
		sample_buffer = np.ones(shape=(23, BUFFER_SIZE), dtype=np.int64)
		arr = bytearray(sample_buffer.nbytes)
		self.buf = memoryview(arr)


BUFFER_SIZE = 10000

reader_process = ReaderProcess(engineType=EngineType.FILE, filename="binary_ivan.dat",
							   freq=500, sync_every=1000, buffer_size=BUFFER_SIZE)

lst = [1, 2]
shm = SharedMemory()

reader_process.run(None, lst, shm)
