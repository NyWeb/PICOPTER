#!/usr/bin/python

import atexit
import signal
import time
import json
import os

# Define controller URLs
commandfile = "/var/www/html/commands/command.json"
logfile = "/var/www/html/commands/log.json"

# Sensor and plugin and motor definitions
sensors = {"location": False, "accelerometer": False, "gyroscope": False, "compass": False, "camera": False, "pwm": False, "alarm": False}
plugins = {"arm": False, "control": False, "location": False, "path": False, "camera": False}
motors = {"throttle":3, "roll":2, "pitch": 1, "jaw": 0, "led":4}

# Handle abortions safely
def abort():
    for plugin in plugins:
        plugins[plugin].cancel()
atexit.register(abort)
signal.signal(signal.SIGTSTP, abort)


# Load all plugins
for plugin in plugins:
    plugins[plugin] = getattr(__import__("plugins."+plugin, fromlist=plugin), plugin)()
    print "plugin ", plugin

# Load all sensors
for sensor in sensors:
    sensors[sensor] = getattr(__import__("sensors."+sensor, fromlist=sensor), sensor)()
    sensors[sensor].start()
    print "sensor ", sensor

# Define counters
error = 0
errorlevel = 10

# Start main runner
while True:
    # Load command file
    if(os.path.isfile(commandfile)):
        holder = open(commandfile)
        command = json.loads(holder.read())
        holder.close()
        os.remove(commandfile)
    else:
        command = {"plugin": False, "parameter": False}

    # Define log
    log = {
        "error": {},
        "sensor": {},
        "plugin": {},
        "control": {}
    }

    # Read data from all sensors
    for sensor in sensors:
        log["sensor"][sensor] = sensors[sensor].read()

        # Check if error exists
        if(sensors[sensor].error):
            if(log["error"]=={}):
                log["error"] = {"sensor": {}}
            log["error"]["sensor"][sensor] = sensors[sensor].error
            sensors[sensor].error = False

    # Go through all plugins
    for plugin in plugins:
        # Command executed to plugin
        if(command['plugin']==plugin):
            log["plugin"][plugin] = plugins[plugin].run(command['parameter'], log["sensor"], sensors)

        elif(error>errorlevel):
            plugins[plugin].emergency(log["sensor"], sensors)

        # Just touch the plugin
        else:
            log["plugin"][plugin] = plugins[plugin].touch(log["sensor"], sensors)

    # Adjust motors based on plugins
    for plugin in plugins:
        if plugin in log["plugin"]:
            if log["plugin"][plugin]:
                for motor in log["plugin"][plugin]:
                    sensors['pwm'].set(motors[motor], log["plugin"][plugin][motor])

    # If log exists, PHP hasn't read it yet. Raise error
    if(os.path.isfile(logfile)):
        error += 1

    # Write log-file
    else:
        try:
            holder = open(logfile, "w")
            json.dump(log, holder)
            holder.close()
            os.chmod(logfile, 0777)
        except OSError:
            print "log file deleted to soon"

    if(log["error"]):
        print log["error"]

    # Give server some chilling-out time
    time.sleep(.01)
