import time

from channels import Channels
from .abstract import AbstractEngine
from .file_engine import FileEngine
from .device_engine import DeviceEngine
from .reader import Reader
from enum import Enum
import numpy as np
from multiprocessing import current_process
import scipy.signal
import pandas as pd 

class EngineType(Enum):
    FILE = 1
    DEVICE = 2

FILTER_ORDER = 100

class ReaderProcess:
    def __init__(self, engineType: EngineType, **options):
        self.engineType = engineType
        self.options = options

    def run(self, lock, shared_list, shared_memory):
        engine: AbstractEngine

        if self.engineType == EngineType.FILE:
            engine = FileEngine(filename=self.options['filename'])
        else:
            engine = DeviceEngine()

        reader = Reader(engine=engine, freq=self.options['freq'])

        frame = 0

        buffer = np.ndarray((23, 0))

        b, a = scipy.signal.iirfilter(4, Wn=45, fs=500, btype="low", ftype="butter")

        while True:
            raw = reader.next()

            if not raw:
                continue

            raw = np.append(np.array(raw), frame).reshape(23, 1)

            buffer = np.append(buffer, raw, axis=1)

            if (buffer.shape[1] > self.options['buffer_size'] + FILTER_ORDER):
                buffer = buffer[:, -(self.options['buffer_size'] + FILTER_ORDER):]

            if (frame + 1) % 500 == 0:
                df = pd.DataFrame(buffer.transpose())
                df.columns = ['F7', 'Fp1', 'Fp2',	'F8', 'F3', 'Fz', 'F4', 'C3', 'Cz', 'P8', 'P7', 'Pz', 'P4', 'T3', 'P3', 'O1', 'O2', 'C4', 'T4', 'A2', 'IMPEDANCE', 'BATTERY', 'FRAME']
                df.to_csv("data/{}.csv".format(frame + 1))

                for i in range(20):
                    filtered = np.ndarray(shape=buffer.shape)
                    filtered[i, :] = scipy.signal.lfilter(b, a, buffer[i, :])

                filtered[20, :] = buffer[20, :]
                filtered[21, :] = buffer[21, :]
                filtered[22, :] = buffer[22, :]

                if lock:
                    lock.acquire()

                shared_list[0] = buffer.shape[0]
                shared_list[1] = buffer.shape[1] - FILTER_ORDER
                shared_memory_array = np.ndarray(shape=(shared_list[0], shared_list[1]), dtype=np.int64, buffer=shared_memory.buf)

                print('write shared memory', shared_memory_array.shape)

                shared_memory_array[:] = filtered[:, FILTER_ORDER:]
                
                if lock:
                    lock.release()

            frame = frame + 1
