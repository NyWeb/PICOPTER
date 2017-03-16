import threading
import RPi.GPIO as GPIO
import time

class alarm(threading.Thread):
    pin = 4

    timespan = 5

    value = False

    error = False

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        timer = 0
        while True:
            # If we've got an alarm beeping
            if not GPIO.input(self.pin):
                # If it beeped X seconds ago
                if(timer>time.time()):
                    # We've got a continuous error
                    self.value = True
                timer = time.time()+self.timespan
            elif time.time()>timer:
                timer = 0
                self.value = False

            time.sleep(.1)

    def read(self):
        return self.value

    def cancel(self, motors):
        return False