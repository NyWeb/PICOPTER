class shell:
    def __init__(self):
        ""

    def touch(self, log, sensors):
        return {"throttle": int(input("throttle")), "pitch": int(input("pitch")), "roll": int(input("roll")), "jaw": int(input("jaw"))}

    def run(self, command, log, sensors):
        ""

    def emergency(self, log, sensors):
        ""

    def cancel(self):
        ""