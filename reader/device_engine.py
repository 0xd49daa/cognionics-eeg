from pylibftdi import Device, SerialDevice
from .abstract import AbstractEngine


class EEGDevice(SerialDevice):
    def __init__(self, *o, **k):
        Device.__init__(self, *o, **k)
        self.baudrate = 3000000
        self.rts = 1


class DeviceEngine(AbstractEngine):
    def __init__(self):
        self.dev = EEGDevice(device_id="AI2NQ43Z", mode="b")

    def read(self, number_of_bytes: int) -> bytes:
        return self.dev.read(number_of_bytes)
