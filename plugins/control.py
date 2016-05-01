class control:
    def __init__(self):
        ""

    def touch(self, log, sensors):
        ""

    def run(self, command, log, sensors):
        return {"throttle": command["left"]["y"], "pitch": command["right"]["y"], "roll": command["right"]["x"], "jaw": command["left"]["x"]}

    def emergency(self, log, sensors):
        ""

    def cancel(self):
        ""