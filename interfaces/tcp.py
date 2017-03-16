import socket
import threading
import time
import json

class tcp(threading.Thread):
    error = False
    port = 7123
    ip = "192.168.1.70"

    outgoing = {}
    incoming = {}

    connection = False

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        type = socket.gethostname()

        while True:
            while not self.connection:
                connection = self.connect(type)

            if type == "picopter":
                try:
                    while self.connection:
                        self.incoming = json.loads(connection.recv(2048))
                        connection.send(json.dumps(self.outgoing))
                except socket.error:
                    self.connection = False
                except ValueError:
                    self.connection = False

            elif type == "controller":
                try:
                    connection.send(json.dumps(self.outgoing))
                    value = connection.recv(2048)

                    if value:
                        self.incoming = json.loads(value)
                        time.sleep(0.01)
                except socket.error:
                    self.connection = False

    def connect(self, type):
        if type == "picopter":
            try:
                holder = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                holder.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                holder.bind(('0.0.0.0', self.port))
                holder.listen(1024)

                connection, address = holder.accept()

                self.connection = True
                return connection

            except socket.error:
                self.connection = False


        elif type == "controller":
            try:
                time.sleep(.1)
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection.connect((self.ip, self.port))

                self.connection = True

                return connection

            except socket.error:
                self.connection = False

    def read(self, log):
        self.outgoing = log
        return self.incoming