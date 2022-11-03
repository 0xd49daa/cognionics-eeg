from sys import prefix
from debug.debug import debug_raw_data
from reader import ReaderProcess, AbstractEngine, EngineType
from plot import draw_process
import multiprocessing
from multiprocessing.managers import SharedMemoryManager
import numpy as np
from multiprocessing import Lock

BUFFER_SIZE = 5000

if __name__ == '__main__':
    lock = Lock()

    with SharedMemoryManager() as smm:
        sample_buffer = np.ones(shape=(23, BUFFER_SIZE), dtype=np.int64)
        sl = smm.ShareableList(range(2))
        shm = smm.SharedMemory(size=sample_buffer.nbytes)

        reader_process = ReaderProcess(engineType=EngineType.DEVICE, filename="binary_ivan.dat", freq=500, buffer_size = BUFFER_SIZE, prefix = "device1", skip_sleep=True)

        reader = multiprocessing.Process(target=reader_process.run, args=(lock, sl, shm, ))
        debug = multiprocessing.Process(target=debug_raw_data, args=(lock, sl, shm, ))
        plot = multiprocessing.Process(target=draw_process, args=(lock, sl, shm, ))

        reader.start()
        debug.start()
        plot.start()

        reader.join()
        debug.join()
        plot.join()

