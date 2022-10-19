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
    def __init__(self, engine, freq):
        self.engine = engine
        self.first_read = False
        self.previous_call = 0
        self.interval = 1.0 / freq

    def read_until_first_byte(self):
        while True:
            byte = self.engine.read(1)
            if byte == b'\xff':
                break

    def next(self) -> list[int]:
        length_to_read = 66
        offset = 2

        if not self.first_read:
            self.read_until_first_byte()
            self.first_read = True
            length_to_read = 65
            offset = 1

        packet = self.engine.read(length_to_read)

        if len(packet) != length_to_read:
            return None

        if (time.perf_counter() - self.previous_call) < self.interval:
            time.sleep((self.interval -(time.perf_counter() - self.previous_call)) / 1.245)

        self.previous_call = time.perf_counter()

        return read_raw(packet, offset)


def read_raw(packet: bytes, offset: int) -> list[int]:
    raw = []

    for channel in range(0, 20):
        raw.append(combine_long(packet, channel * 3 + offset))

    return raw


def combine_long(packet: bytes, start_byte: int) -> int:
    msb = packet[start_byte]
    lsb2 = packet[start_byte + 1]
    lsb1 = packet[start_byte + 2]

    return (msb << 24) | (lsb2 << 17) | (lsb1 << 10)
