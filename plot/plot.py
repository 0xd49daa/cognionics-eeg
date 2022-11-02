import matplotlib.pyplot as plt
import numpy as np
from .rescale import rescale_axis
from time import sleep

from channels import Channels

def draw_process(lock, sl, shm):
	plt.ion()
	fig, ax = plt.subplots(2, figsize=(25, 5))

	channel0_data = np.ndarray([])
	channel1_data = np.ndarray([])
	time_data = np.ndarray([])

	channel0, = ax[0].plot(time_data, channel0_data)
	channel1, = ax[1].plot(time_data, channel1_data)
	
	ax[0].set_title('O1')
	ax[0].set_xlabel('Time (s)')

	ax[1].set_title('O2')
	ax[1].set_xlabel('Time (s)')

	while True:
		dim = (sl[0], sl[1])
		shared_memory_array = np.ndarray(dim, dtype=np.int64, buffer=shm.buf)

		if shared_memory_array.shape[0] != 23:
			plt.pause(0.25)
			continue

		if lock:
			lock.acquire()

		channel0_data = shared_memory_array[Channels.O1, :]
		channel1_data = shared_memory_array[Channels.O2, :]
		time_data = shared_memory_array[Channels.FRAME, :] / 500

		# print("shared_memory_array", shared_memory_array.shape)
		# print("channel0_data", channel0_data.shape)
		# print("time_data", time_data.shape)

		if lock:
			lock.release()

		channel0.set_xdata(time_data)
		channel0.set_ydata(channel0_data)

		channel1.set_xdata(time_data)
		channel1.set_ydata(channel1_data)

		rescale_axis(ax[0], time_data, 10)
		rescale_axis(ax[1], time_data, 10)

		# print(time_data)
		# print(channel0_data)

		fig.canvas.draw()
		fig.canvas.flush_events()

		plt.pause(0.25)
