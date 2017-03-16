import threading
import time
import RPi.GPIO as GPIO

class sonar(threading.Thread):
    echo = 20
    trigger = 21

    mach = 17150
    limit = 400

    value = 0

    kalman = 0.8
    filter1 = 0
    filter2 = 0

    level = 0
    errorlevel = 5
    error = False

    def __init__(self, address=0x68):
        threading.Thread.__init__(self)
        self.daemon = True

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

        GPIO.output(self.trigger, False)
        time.sleep(2)

    def run(self):
        while True:
            self.get()

            if self.level>self.errorlevel:
                self.error = "reading_error"
                print self.error

            time.sleep(.01)

    def get(self):
        GPIO.output(self.trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)

        # Pause whilst sensor is fetching, but escape if we've got a fault
        i = 0
        while GPIO.input(self.echo)==0:
            if i>100:
                self.level += 1
                return
            i += 1

        start = time.time()

        # Pause until sensor is done, but escape if we've not got a huge fault
        i = 0
        stop = 0
        while GPIO.input(self.echo)==1:
            if i>10000:
                self.level += 1
                return
            i += 1

        distance = round((time.time()-start)*self.mach, 2)
        if distance>self.limit:
            self.level += 1
            return

        self.level = 0
        self.error = False

        self.value = (distance*(1-self.kalman)) + ((self.filter1+(self.filter1-self.filter2))*self.kalman)

        self.filter2 = self.filter1
        self.filter1 = self.value

    def read(self):
        return self.value

    def cancel(self, motors):
        return False