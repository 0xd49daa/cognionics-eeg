import numpy as np

def morlet_data_process(current_morlet_lock, current_morlet_sl, morlet_data_lock, morler_shape, morlet_data):
	with current_morlet_lock:
		frame = current_morlet_sl[0]
		value12 = current_morlet_sl[1]
		value15 = current_morlet_sl[2]


	with morlet_data_lock:
		shared_memory_array = np.ndarray(shape=shape, dtype=np.int64, buffer=shm.buf)
		local_data = np.ndarray(shape=shape, dtype=np.int64)
		local_data[:,:] = shared_memory_array[:,:]
