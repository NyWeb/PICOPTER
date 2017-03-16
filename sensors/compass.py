import threading
import smbus
from math import pi, degrees, atan2
import time

class compass(threading.Thread):
    address = None
    bus = None

    value = {}

    gain = 0.92

    error = False

    math = False

    kalman = 0.5
    filter1 = False
    filter2 = False

    def __init__(self, address=0x1e):
        threading.Thread.__init__(self)
        self.daemon = True

        self.bus = smbus.SMBus(1)
        self.address = address

        try:
            self.bus.write_byte_data(self.address, 0, 0b01110000)
            self.bus.write_byte_data(self.address, 1, 0b00100000)
            self.bus.write_byte_data(self.address, 2, 0b00000000)

        except IOError:
            self.error = "ioerror initialize"
            return

    def run(self):
        while True:
            self.value = self.get()
            time.sleep(.1)

    def get(self):
        try:
            x = self.combine(self.bus.read_byte_data(self.address, 3), self.bus.read_byte_data(self.address, 4))*self.gain
            y = self.combine(self.bus.read_byte_data(self.address, 7), self.bus.read_byte_data(self.address, 8))*self.gain
            z = self.combine(self.bus.read_byte_data(self.address, 5), self.bus.read_byte_data(self.address, 6))*self.gain

            # Kalman filter
            if(self.filter2):
                x = (x*(1-self.kalman)) + ((self.filter1["x"]+(self.filter1["x"]-self.filter2["x"]))*self.kalman)
                y = (y*(1-self.kalman)) + ((self.filter1["y"]+(self.filter1["y"]-self.filter2["y"]))*self.kalman)
                z = (z*(1-self.kalman)) + ((self.filter1["z"]+(self.filter1["z"]-self.filter2["z"]))*self.kalman)

            x = round(x, 1)
            y = round(y, 1)
            z = round(z, 1)

            self.filter2  = self.filter1
            self.filter1  = {"x": x, "y": y, "z": z}

            bearing = atan2(y, x)
            if (bearing < 0):
                bearing += 2 * pi

            bearing = degrees(bearing)

        except IOError:
            self.error = "ioerror"
            return self.value

        return {"bearing": bearing, "x": x, "y": y, "z": z}

    def read(self):
        return self.value

    def combine(self, msb, lsb):
        twos_comp = 256*msb+lsb
        if twos_comp >= 32768:
            return twos_comp - 65536
        else:
            return twos_comp

    def cancel(self, motors):
        return False