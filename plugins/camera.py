class camera:
    def __init__(self):
        ""

    def touch(self, interface, log, sensors, plugin):
        ""

    def run(self, interface, log, sensors, plugin):
        if(interface==sensors["camera"].action):
            sensors["camera"].action = ""
        else:
            sensors["camera"].action = interface

    def emergency(self, log, sensors):
        ""

    def cancel(self):
        ""