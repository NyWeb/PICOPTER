#!/usr/bin/python

import atexit
import signal
import time
import json
import socket

# Define controller URLs
logfile = "/var/www/html/log/log.json"

# Sensor and plugin and motor definitions, for PiCopter
if socket.gethostname() == "picopter":
    interfaces = {"file": False, "tcp": False}
    sensors = {"sonar": False, "wifi": False, "pwm": False, "location": False, "accelerometer": False, "gyroscope": False, "compass": False, "camera": False, "alarm": False}
    plugins = {"location": False, "path": False, "camera": False, "gimbal": False, "control": False, "arm": False}
    motors = {"throttle":4, "roll":3, "pitch": 2, "yaw": 1, "aux":0, "gimbal_y":5, "gimbal_z": 6, "gimbal_x": 7}

# Sensor and plugin and motor definitions, for the controller
elif socket.gethostname() == "controller":
    interfaces = {"tcp": False}
    sensors = {"accelerometer": False, "gyroscope": False, "compass": False, "joystick": False, "wifi": False}
    plugins = {"headset": False}
    motors = {}

# Handle abortions safely
def abort():
    for sensor in sensors:
        sensors[sensor].cancel(motors)
    for plugin in plugins:
        plugins[plugin].cancel()
atexit.register(abort)
signal.signal(signal.SIGTSTP, abort)

# Load all interfaces
for interface in interfaces:
    interfaces[interface] = getattr(__import__("interfaces."+interface, fromlist=interface), interface)()
    interfaces[interface].start()
    print "interface ", interface

# Load all sensors
for sensor in sensors:
    sensors[sensor] = getattr(__import__("sensors."+sensor, fromlist=sensor), sensor)()
    sensors[sensor].start()
    print "sensor ", sensor

# Load all plugins
for plugin in plugins:
    plugins[plugin] = getattr(__import__("plugins."+plugin, fromlist=plugin), plugin)()
    print "plugin ", plugin

# Define error-counters
error = 0
lasterror = 0
errorlevel = 10

try:

    # Start main runner
    while True:
        # Define log
        log = {
            "error": {},
            "interface": {},
            "sensor": {},
            "plugin": {}
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


        # Read data from all interfaces
        for interface in interfaces:
            log["interface"][interface] = interfaces[interface].read(log['sensor'])

            # Check if error exists
            if interfaces[interface].error:
                error += 1

                # If error isn't defined in matrix, it needs to be that now
                if log["error"] == {}:
                    log["error"] = {"interface": {}}

                # Save error to log, and remove it for next run
                log["error"]["interface"][interface] = interfaces[interface].error
                interfaces[interface].error = False

        # Go through all plugins
        for plugin in sorted(plugins):
            active = False

            # Command executed to plugin
            for interface in interfaces:
                # Did the interface mention this plugin?
                if hasattr(log['interface'][interface], 'plugin') and hasattr(log['interface'][interface]['plugin'], plugin):
                    active = True

            # This plugin is actively called from the interface
            if active:
               log["plugin"][plugin] = plugins[plugin].run(log['interface'], log["sensor"], sensors, log["plugin"])

            # There's an error, so we must run the emergency protocol on this plugin
            elif error > errorlevel:
                plugins[plugin].emergency(log["sensor"], sensors)

            # Just touch the plugin, as it's neither active, nor do we have an emergency
            else:
                log["plugin"][plugin] = plugins[plugin].touch(log['interface'], log["sensor"], sensors, log["plugin"])

        # Adjust motors based on plugins
        for plugin in plugins:
            if plugin in log["plugin"]:
                if log["plugin"][plugin]:
                    if 'motor' in log["plugin"][plugin]:
                        for motor in log["plugin"][plugin]["motor"]:
                            sensors['pwm'].set(motors[motor], log["plugin"][plugin]["motor"][motor])

        # If error-level hasn't changed, we need to reset error counter
        if error == lasterror:
            error = 0

        # Save error-counter for next round
        lasterror = error

        # Log if we've got an error above what's allowed
        if error > errorlevel:
            log["error"] = {"pilot": {}}

        # Write log-file
        holder = open(logfile, "w")
        json.dump(log, holder)
        holder.close()

        # Give server some chilling-out time
        time.sleep(.01)
except KeyboardInterrupt:
    abort()