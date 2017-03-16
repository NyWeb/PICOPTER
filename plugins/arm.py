class arm:
    status = False
    level = False

    def __init__(self):
        ""

    def touch(self, interface, log, sensors, plugin):
        return self.run(interface, log, sensors, plugin)

    def run(self, interface, log, sensors, plugin):
        "Check that both buttons are pressed, and if they are, arm this!"
        if 'joystick' in interface['tcp']:
            # If both buttons are pressed
            if interface['tcp']['joystick']['left_button']==100 and interface['tcp']['joystick']['right_button']==100:
                # Last time, we weren't arming!
                if not self.status:
                    self.status = True

                    # If we used to be on, let's disarm
                    if self.level:
                        self.level = False
                        print "Disarming!"
                        return {"motor":{"throttle":0, "yaw": 100}}

                    # Otherwise, we must arm
                    else:
                        self.level = True
                        print "Arming!"
                        return {"motor":{"throttle":0, "yaw": 0}}

            else:
                if self.status:
                    self.status = False

                if not self.level:
                    print "Passive disarming!"
                    return {"motor":{"throttle":0, "yaw": 100}}
                else:
                    return False

    def emergency(self, log, sensors):
        ""

    def cancel(self):
        ""