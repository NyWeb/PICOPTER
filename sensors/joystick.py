import threading
import time
import spidev

class joystick(threading.Thread):
    x1 = 0
    y1 = 0
    z1 = 0

    x2 = 0
    y2 = 0
    z2 = 0

    bus = False
    spi = False

    value = []

    error = False

    map = {0: False, 1: False, 2: {"name":"right_button", "direction":-1}, 3: {"name":"right_y", "direction":1}, 4: {"name":"right_x", "direction":1}, 5: {"name":"left_button", "direction":-1}, 6: {"name":"left_y", "direction": -1}, 7: {"name":"left_x", "direction":-1}}

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz=1000000
        self.spi.mode = 0
        self.spi.lsbfirst = False

    def run(self):
        self.value = {}
        while True:
            for i in range(8):
                if self.map[i]:
                    value = self.get(i)
                    if self.map[i]['direction']==-1:
                        value = round((1024-value)/10.24)
                    else:
                        value = round(value/10.24)
                    self.value[self.map[i]['name']] = value
            time.sleep(0.05)

    def get(self, number):
        command = 0b11 << 6
        command |= (number & 0x07) << 3

        resp = bytearray(self.spi.xfer2([command, 0x0, 0x0]))
        result = (resp[0] & 0x01) << 9
        result |= (resp[1] & 0xFF) << 1
        result |= (resp[2] & 0x80) >> 7
        return result & 0x3FF

    def read(self):
        return self.value

    def cancel(self, motors):
        return False