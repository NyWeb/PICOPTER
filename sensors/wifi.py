import threading
import RPi.GPIO as GPIO
import socket
import time

class wifi(threading.Thread):
    pin = 13
    error = False
    last = False

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        state = GPIO.input(self.pin)
        if state != self.last:
            if state:
                if socket.gethostname()=="picopter":
                    """"""
                else:
                    """"""

            else:
                if socket.gethostname()=="picopter":
                    """"""
                else:
                    """"""

        self.last = state

    def read(self):
        return False

    def cancel(self, motors):
        return False