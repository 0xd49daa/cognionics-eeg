import time
import numpy as np

from channels import Channels

def debug_raw_data(lock, sl, shm):
	while True:		
		dim = (sl[0], sl[1])

		if lock:
			lock.acquire()

		shared_memory_array = np.ndarray(dim, dtype=np.int64, buffer=shm.buf)

		# count = sl[Channels.FRAME]

		# print("{} Frames per second...".format(count - prev_count))

		# prev_count = count
		if (shared_memory_array.shape[0] == 23):
			print("Debug data: ", shared_memory_array.shape, shared_memory_array[Channels.IMPEDANCE, :])

		if lock:
			lock.release()

		time.sleep(1)
