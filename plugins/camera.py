class camera:
    def __init__(self):
        ""

    def touch(self, log, sensors):
        ""

    def run(self, command, log, sensors):
        if(command==sensors["camera"].action):
            sensors["camera"].action = ""
        else:
            sensors["camera"].action = command

    def emergency(self, log, sensors):
        ""

    def cancel(self):
        ""