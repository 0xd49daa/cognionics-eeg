# 0xFF start byte
# 0x31 count byte
# 60 bytes / 3 bytes per channel / 20 channels
# 0x11 impedance byte check
# battery voltage
# trigger msb
# trigger lsb
# 66 bytes in summary
import time

class Reader:
    def __init__(self, engine, freq, skip_sleep = False):
        self.engine = engine
        self.first_read = False
        self.previous_call = 0
        self.interval = 1.0 / freq
        self.skip_sleep = skip_sleep

    def read_until_first_byte(self):
        count = 0

        while True:
            byte = self.engine.read(1)
            if byte == b'\xff':
                if count > 0:
                    print("skip before next packet start {}".format(count))
                break
            count = count + 1

    def next(self):
        self.read_until_first_byte()
        self.first_read = True
        length_to_read = 65
        offset = 1

        packet = self.engine.read(length_to_read)

        if len(packet) != length_to_read:
            return None

        if not self.skip_sleep:
            if (time.perf_counter() - self.previous_call) < self.interval:
                time.sleep((self.interval -(time.perf_counter() - self.previous_call)))

        self.previous_call = time.perf_counter()

        arr = read_raw(packet, offset)

        return arr



def read_raw(packet: bytes, offset: int):
    raw = []

    for channel in range(0, 20):
        raw.append(combine_long(packet, channel * 3 + offset))

    raw.append(packet[offset + 60])
    raw.append(packet[offset + 61])

    return raw


def combine_long(packet: bytes, start_byte: int) -> int:
    msb = packet[start_byte]
    lsb2 = packet[start_byte + 1]
    lsb1 = packet[start_byte + 2]

    return (msb << 24) | (lsb2 << 17) | (lsb1 << 10)
