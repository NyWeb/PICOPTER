import random
import time

class gimbal:
    level = False
    gyroscope = 0.9
    status = False

    def __init__(self):
        ""

    def touch(self, interface, log, sensors, plugin):
        return self.run(interface, log, sensors, plugin)


    def run(self, interface, log, sensors, plugin):
        "Check that we're armed!"
        # Check if we're flying
        if log['sonar']<40 or plugin['arm']:
            if not self.status:
                return

            # Did we transition?
            if self.level:
                self.level = False
                return {"motor":{"gimbal_y": 200, "gimbal_z": 25, "gimbal_x": 75}}
            else:
                return {"motor":{"gimbal_y": 240, "gimbal_z": -65, "gimbal_x": 75}}

        else:
            self.status = True

            # Did the gimbal just activate?
            if self.level:
                x = ((log['gyroscope']['x']*self.gyroscope)+(log['accelerometer']['x']*(1-self.gyroscope)))
                y = ((log['gyroscope']['y']*self.gyroscope)+(log['accelerometer']['y']*(1-self.gyroscope)))
                z = ((log['gyroscope']['z']*self.gyroscope)+(log['accelerometer']['z']*(1-self.gyroscope)))

                return {"motor":{"gimbal_y": 100+(y), "gimbal_z": 50+(x), "gimbal_x": 50+(z)}}
            else:
                self.level = True
                return {"motor":{"gimbal_y": 200, "gimbal_z": 25, "gimbal_x": 75}}

    def emergency(self, log, sensors):
        ""

    def cancel(self):
        ""