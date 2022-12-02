import numpy as np
from multiprocessing import Lock
from multiprocessing.managers import SharedMemoryManager
from morlet import morlet_process

if __name__ == '__main__':
	with SharedMemoryManager() as smm:
		buffer_size = 5000

		lock_o1_morlet = Lock()
		lock_o2_morlet = Lock()
		lock = Lock()

		sl_o1_morlet = smm.ShareableList(range(3))
		sl_o1_morlet[0] = 0 # time
		sl_o1_morlet[1] = 0 # morlet 12
		sl_o1_morlet[2] = 0 # morlet 15

		sl_o2_morlet = smm.ShareableList(range(3))
		sl_o2_morlet[0] = 0 # time
		sl_o2_morlet[1] = 0 # morlet 12
		sl_o2_morlet[2] = 0 # morlet 15

		shape = (24, buffer_size)

		sample_buffer = np.ones(shape=shape, dtype=np.int64)
		sl = smm.ShareableList(range(2))
		shm = smm.SharedMemory(size=sample_buffer.nbytes)

		random_array = np.random.randint(low=10, high=5000, size=shape)
		shared_memory_array = np.ndarray(shape=shape, dtype=np.int64, buffer=shm.buf)
		shared_memory_array[:, :] = random_array[:, :]

		sl[0] = 24
		sl[1] = buffer_size

		morlet_process(lock_o1_morlet, sl_o1_morlet, lock_o2_morlet, sl_o2_morlet, lock, shm, sl)
