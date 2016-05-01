import threading
import smbus

class pwm(threading.Thread):
    bus = False
    address = False

    k = 2
    m = 294

    error = False

    def __init__(self, address=0x40):
        threading.Thread.__init__(self)
        self.daemon = True

        self.bus = smbus.SMBus(1)
        self.address = address

        try:
            self.bus.write_byte_data(self.address, 0x01, 0x04)
            mode1 = self.bus.read_byte_data(self.address, 0x00)
            mode1 = mode1 & ~0x10
            self.bus.write_byte_data(self.address, 0x00, mode1)
            oldmode = self.bus.read_byte_data(self.address, 0x00)
            newmode = (oldmode & 0x7F) | 0x10
            self.bus.write_byte_data(self.address, 0x00, newmode)
            self.bus.write_byte_data(self.address, 0xFE, 100)
            self.bus.write_byte_data(self.address, 0x00, oldmode)
            self.bus.write_byte_data(self.address, 0x00, oldmode | 0x80)

        except IOError:
            self.error = "ioerror initialize"
            return

    def run(self):
        return False

    def read(self):
        return False

    def set(self, motor, torque):
        input = int(((torque)*self.k)+self.m)

        try:
            self.bus.write_byte_data(self.address, 0x06+4*motor, 0 & 0xFF)
            self.bus.write_byte_data(self.address, 0x07+4*motor, 0 >> 8)
            self.bus.write_byte_data(self.address, 0x08+4*motor, input & 0xFF)
            self.bus.write_byte_data(self.address, 0x09+4*motor, input >> 8)

        except IOError:
            self.error = "ioerror"