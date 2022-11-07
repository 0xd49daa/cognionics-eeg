from .abstract import AbstractEngine
from .file_engine import FileEngine
from .device_engine import DeviceEngine
from .reader import Reader
from enum import Enum
import numpy as np
from multiprocessing import current_process
from datetime import datetime
from io import open
from os import linesep

COLUMNS = ['F7', 'Fp1', 'Fp2',	'F8', 'F3', 'Fz', 'F4', 'C3', 'Cz', 'P8', 'P7', 'Pz', 'P4', 'T3', 'P3', 'O1', 'O2', 'C4', 'T4', 'A2', 'IMPEDANCE', 'BATTERY', 'DEVICE_COUNT', 'FRAME']
FOLDER = "parsed/"

class EngineType(Enum):
    FILE = 1
    DEVICE = 2

class ReaderProcess:
    def __init__(self, engineType: EngineType, **options):
        self.engineType = engineType
        self.options = options

    def generate_filename(self):
        return self.engineType.name + "-" + datetime.now().strftime("%d-%m-%y-%H-%M-%S") + ".csv"


    def run(self, lock, shared_list, shared_memory):
        engine: AbstractEngine

        if self.engineType == EngineType.FILE:
            engine = FileEngine(filename=self.options['filename'])
        else:
            engine = DeviceEngine()

        reader = Reader(engine=engine, freq=self.options['freq'], skip_sleep=self.options['skip_sleep'])

        frame = 0

        buffer = np.ndarray((24, 0))

        file = open(FOLDER + self.generate_filename(), mode='w')

        file.write(','.join(COLUMNS) + linesep)

        while True:
            raw = reader.next()

            if not raw:
                break

            raw = np.append(np.array(raw), frame).reshape(24, 1)
            l = raw.reshape(24,).tolist()

            file.write(','.join(str(value) for value in l) + linesep)

            buffer = np.append(buffer, raw, axis=1)

            if (buffer.shape[1] > self.options['buffer_size']):
                buffer = buffer[:, -(self.options['buffer_size']):]

            if (frame + 1) % 500 == 0:
                file.flush()

                if lock:
                    lock.acquire()

                shared_list[0] = buffer.shape[0]
                shared_list[1] = buffer.shape[1]
                shared_memory_array = np.ndarray(shape=(shared_list[0], shared_list[1]), dtype=np.int64, buffer=shared_memory.buf)

                print('write shared memory', shared_memory_array.shape)

                shared_memory_array[:] = buffer[:, :]
                
                if lock:
                    lock.release()

            frame = frame + 1

        file.close()
