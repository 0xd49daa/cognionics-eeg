import time
from .abstract import AbstractEngine
from .reader import Reader

class ReaderProcess:
    def __init__(self, data_exchange, engine: AbstractEngine, freq=500, sync_every=1000):
        self.data_exchange = data_exchange
        self.engine = engine
        self.freq = freq
        self.sync_every = sync_every

    def run(self):
        reader = Reader(engine=self.engine, freq=self.freq)

        prev = time.perf_counter()
        count = 0
        time_in_frames = self.sync_every / self.freq

        while True:
            raw = reader.next()

            if not raw:
                self.data_exchange['raw'] = None
                continue

            self.data_exchange['raw'] = raw

            if count % self.sync_every == 0:
                print(raw)
                time_in_real = time.perf_counter() - prev

                print("Got {} frames in {} seconds".format(self.sync_every, time_in_real))

                if time_in_frames > time_in_real:
                    print("Frames faster than real time {}%".format(100 * (time_in_frames / time_in_real - 1)))
                else:
                    print("Frames slower than real time {}%".format(100 * (time_in_real / time_in_frames - 1)))

                prev = time.perf_counter()

            count = count + 1
