class arm:
    status = 0

    def __init__(self):
        ""

    def touch(self, log, sensors):
        ""

    def run(self, command, log, sensors):
        if self.status:
            self.status = 0
            return {"throttle": 0, "pitch": 50, "roll": 50, "jaw": 100}
        else:
            self.status = 1
            return {"throttle": 0, "pitch": 50, "roll": 50, "jaw": 0}

    def emergency(self, log, sensors):
        ""

    def cancel(self):
        ""