import threading
import gps
import time
from math import radians, sin, cos, atan2, sqrt

class location(threading.Thread):
    session = False

    latitude = False
    longitude = False
    altitidue = False

    value = {}

    error = False

    radius = 6371000

    kalman = 0.5
    filter1 = False
    filter2 = False

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        try:
            self.session = gps.gps(mode=gps.WATCH_ENABLE)

        except IOError:
            self.error = "ioerror initialize"
            return

    def run(self):
        while True:
            try:
                self.session.next()
                if(self.session.fix.latitude):
                    # Get values
                    latitude = self.session.fix.latitude
                    longitude = self.session.fix.longitude
                    altitude = self.session.fix.altitude
                    distance = 0

                    # Kalman filter
                    if(self.filter2):
                        latitude = (latitude*(1-self.kalman)) + ((self.filter1["latitude"]+(self.filter1["latitude"]-self.filter2["latitude"]))*self.kalman)
                        longitude = (longitude*(1-self.kalman)) + ((self.filter1["longitude"]+(self.filter1["longitude"]-self.filter2["longitude"]))*self.kalman)
                        altitude = (altitude*(1-self.kalman)) + ((self.filter1["altitude"]+(self.filter1["altitude"]-self.filter2["altitude"]))*self.kalman)

                        # If latitude isn't set
                        if(self.latitude==False):
                            self.latitude = round(latitude, 6)
                            self.longitude = round(longitude, 6)
                            self.altitude = round(altitude, 6)
                        else:
                            distance = self.distance(latitude, longitude, altitude)

                    latitude = round(latitude, 6)
                    longitude = round(longitude, 6)
                    altitude = round(altitude, 6)
                    distance = round(distance, 1)

                    self.filter2 = self.filter1
                    self.filter1 = {"latitude": latitude, "longitude": longitude, "altitude": altitude, "distance": distance}

                    self.value = {"latitude": latitude, "longitude": longitude, "altitude": altitude, "distance": distance}

            except IOError:
                self.error = "ioerror"

            time.sleep(1)

    def read(self):
        return self.value

    def distance(self, latitude, longitude, altitude):
        x = (self.longitude-longitude)*cos(0.5*(self.latitude+latitude))
        y = self.latitude-latitude
        distance2d = self.radius*sqrt(x*x+y*y)
        return sqrt(distance2d*distance2d+((self.altitidue-altitude)*(self.altitidue-altitude)))

    def cancel(self, motors):
        return False