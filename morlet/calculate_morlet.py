from time import sleep
import numpy as np
from channels import Channels
from .wavelet import morlet_convolution

WIDTH = 4
N_CYCLES = 80
SRATE = 500

def copy_data(shape, shm):
	shared_memory_array = np.ndarray(shape=shape, dtype=np.int64, buffer=shm.buf)
	local_data = np.ndarray(shape=shape, dtype=np.int64)
	local_data[:,:] = shared_memory_array[:,:]

	return local_data


def calculate_morlet(local_data, channelIndex, lock_morlet, sl_morlet):
	from_index, to_index = local_data.shape[1] - WIDTH * SRATE, local_data.shape[1]	
	data_for_morlet_calculation = local_data[channelIndex, from_index:to_index]

	frame = local_data[Channels.FRAME, int((to_index - from_index) / 2)]

	value12 = morlet_convolution(data_for_morlet_calculation, SRATE, N_CYCLES, 12, WIDTH)
	value12 = np.float_power(np.abs(value12), 2.)

	value15 = morlet_convolution(data_for_morlet_calculation, SRATE, N_CYCLES, 15, WIDTH)
	value15 = np.float_power(np.abs(value15), 2.)

	with lock_morlet:
		sl_morlet[0] = int(frame)
		sl_morlet[1] = int(value12)
		sl_morlet[2] = int(value15)


def morlet_process(lock_o1_morlet, sl_o1_morlet, lock_o2_morlet, sl_o2_morlet, lock, shm, sl):
	while True:
		with lock:
			if sl[1] > WIDTH * SRATE:
				local_data = copy_data((sl[0], sl[1]), shm)

		if sl[1] > WIDTH * SRATE:
			calculate_morlet(local_data, Channels.O1, lock_o1_morlet, sl_o1_morlet)
			calculate_morlet(local_data, Channels.O2, lock_o2_morlet, sl_o2_morlet)

