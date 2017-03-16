import threading
import smbus
import time

class gyroscope(threading.Thread):
    address = None
    bus = None

    x = 0
    y = 0
    z = 0

    value = {}

    radsec2degsec = 14.375

    error = False

    kalman = 0.5
    filter1 = False
    filter2 = False

    def __init__(self, address=0x68):
        threading.Thread.__init__(self)
        self.daemon = True

        self.bus = smbus.SMBus(1)
        self.address = address

        try:
            self.bus.write_byte_data(self.address, 0x16, 0x18|0x00)
            self.bus.write_byte_data(self.address, 0x3E, 0x01)
            self.bus.write_byte_data(self.address, 0x15, 0x00)
            self.bus.write_byte_data(self.address, 0x20, 0x04|0x01)

        except IOError:
            self.error = "ioerror initialize"
            return

    def run(self):
        while True:
            self.value = self.get()
            time.sleep(.1)

    def get(self):
        try:
            x = self.combine(self.bus.read_byte_data(self.address, 0x1D), self.bus.read_byte_data(self.address, 0x1E))/self.radsec2degsec
            y = self.combine(self.bus.read_byte_data(self.address, 0x1F), self.bus.read_byte_data(self.address, 0x20))/self.radsec2degsec
            z = self.combine(self.bus.read_byte_data(self.address, 0x21), self.bus.read_byte_data(self.address, 0x22))/self.radsec2degsec

            # Kalman filter
            if(self.filter2):
                x = (x*(1-self.kalman)) + ((self.filter1["x"]+(self.filter1["x"]-self.filter2["x"]))*self.kalman)
                y = (y*(1-self.kalman)) + ((self.filter1["y"]+(self.filter1["y"]-self.filter2["y"]))*self.kalman)
                z = (z*(1-self.kalman)) + ((self.filter1["z"]+(self.filter1["z"]-self.filter2["z"]))*self.kalman)
                if self.x==False:
                    self.x = round(x, 2)
                    self.y = round(y, 2)
                    self.z = round(z, 2)

            x = round(x, 2)
            y = round(y, 2)
            z = round(z, 2)

            self.filter2  = self.filter1
            self.filter1  = {"x": x, "y": y, "z": z}

            x -= float(self.x)
            y -= float(self.y)
            z -= float(self.z)

        except IOError:
            self.error = "ioerror"
            return self.value

        return {"x": x, "y": y, "z": z}

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