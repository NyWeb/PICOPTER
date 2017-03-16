class control:
    throttle = 0
    height = 0

    def __init__(self):
        ""

    def touch(self, interface, log, sensors, plugin):
        return self.run(interface, log, sensors, plugin)

    def run(self, interface, log, sensors, plugin):
        if 'joystick' in interface['tcp']:
            throttle = (interface['tcp']['joystick']['left_y']-100)*2

            # Are we increasing height?
            self.height += (throttle/100)

            # Is the height lower than safe?
            if self.height < 40:
                self.height = 40

            # If we're above max of what sensor can take
            elif self.height > 400:
                self.height = 400

            # If we're higher than wished
            self.throttle += (self.height-sensors['sonar'])/100

            if self.throttle<20:
                self.throttle = 20

            elif self.throttle>100:
                self.throttle = 100

            return {"motor":{"throttle":self.throttle, "roll": interface['tcp']['joystick']['right_x'], "pitch": interface['tcp']['joystick']['right_y'], "yaw": interface['tcp']['joystick']['left_x']}}

    def emergency(self, log, sensors):
        ""

    def cancel(self):
        ""