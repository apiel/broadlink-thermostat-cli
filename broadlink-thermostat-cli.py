#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys
import broadlink  # pip install broadlink
import json  # pip install json

def main():
    # print "The arguments are: " , str(args)
    print "broadlink discover"
    print "Usage: --mode=manual --temp=22 --power=on"
    print "--mode=auto|manual"
    print "--mode2=auto|manual"
    print "--temp=22"
    print "--power=on|off"
    print "--schedule='[{\"start_hour\":6,\"temp\":23.0,\"start_minute\":0}]'"
    # ./broadlink-thermostat-cli.py --schedule='[{"start_hour":6,"temp":23.0,"start_minute":0},{"start_hour":23,"temp":15.0,"start_minute":0}]'
    args = [arg.split('=', 1) for arg in sys.argv[1:]]

    devices = broadlink.discover(timeout=5)
    for device in devices:
        print "found: {} {}".format(device.host[0], ''.join(format(x, '02x') for x in device.mac))
        if device.auth():
            for arg in args:
                if arg[0] == "--mode":
                    device.set_mode(0 if arg[1] == "auto" else 1, 0) # ("12345,67")
                elif arg[0] == "--mode2":
                    device.set_mode(0 if arg[1] == "auto" else 1, 2) # ("1234567")
                elif arg[0] == "--temp":
                    device.set_temp(float(arg[1]))
                elif arg[0] == "--power":
                    device.set_power(0 if arg[1] == "off" else 1, 0)
                elif arg[0] == "--schedule":
                    schedules=json.loads(arg[1])
                    if len(schedules) != 2:
                        print "schedule should contain 2 value, start and end."
                    else:
                        schedules = [schedules[0], schedules[1], schedules[1], schedules[1], schedules[1], schedules[1]] # the thermostat is expecting 6 values but 2 are enough
                        device.set_schedule(schedules, schedules)
            print device.type
        else:
            print "error: could not auth"
    print "done"
    return

main()
