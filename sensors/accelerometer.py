import threading
import smbus
import time

class accelerometer(threading.Thread):
    address = None
    bus = None

    x = False
    y = False
    z = False

    value = {}

    angle2radian = 57.29578
    magic = 1.33#9.80665

    error = False

    kalman = 0.9
    filter1 = False
    filter2 = False

    def __init__(self, address=0x53):
        threading.Thread.__init__(self)
        self.daemon = True

        self.bus = smbus.SMBus(1)
        self.address = address

        try:
            self.bus.write_byte_data(self.address, 0x2C, 0x0E)
            value = self.bus.read_byte_data(self.address, 0x31)
            value &= ~0x0F
            value |= 0x00
            value |= 0x08
            self.bus.write_byte_data(self.address, 0x31, value)
            self.bus.write_byte_data(self.address, 0x2D, 0x08)

        except:
            self.error = "ioerror initialize"
            return

    def run(self):
        while True:
            self.value = self.get()
            time.sleep(.1)

    def get(self):
        try:
            bytes = self.bus.read_i2c_block_data(self.address, 0x32, 6)

            x = bytes[0] | (bytes[1] << 8)
            if x & (1 << 16 - 1):
                x -= (1 << 16)

            y = bytes[2] | (bytes[3] << 8)
            if y & (1 << 16 - 1):
                y -= ( 1 << 16 )

            z = bytes[4] | (bytes[5] << 8)
            if z & (1 << 16 - 1):
                z -= ( 1 << 16 )

            x *= 0.004*self.magic*self.angle2radian
            y *= 0.004*self.magic*self.angle2radian
            z *= 0.004*self.magic*self.angle2radian

            # Kalman filter
            if(self.filter2):
                x = (x*(1-self.kalman)) + ((self.filter1["x"]+(self.filter1["x"]-self.filter2["x"]))*self.kalman)
                y = (y*(1-self.kalman)) + ((self.filter1["y"]+(self.filter1["y"]-self.filter2["y"]))*self.kalman)
                z = (z*(1-self.kalman)) + ((self.filter1["z"]+(self.filter1["z"]-self.filter2["z"]))*self.kalman)
                if self.x==False:
                    self.x = x
                    self.y = y
                    self.z = z

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

    def cancel(self, motors):
        return False