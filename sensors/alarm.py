import threading

class alarm(threading.Thread):
    error = False

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        return False

    def read(self):
        return False