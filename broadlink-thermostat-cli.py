#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys
import broadlink  # pip install broadlink

def main():
    # print "The arguments are: " , str(args)
    print "broadlink discover"
    print "Usage: --mode=auto --temp=22 --power=on"
    print "Usage: --mode=manual --temp=15 --power=off"
    args = [arg.split('=', 1) for arg in sys.argv[1:]]

    devices = broadlink.discover(timeout=5)
    for device in devices:
        print "found: {} {}".format(device.host[0], ''.join(format(x, '02x') for x in device.mac))
        if device.auth():
            for arg in args:
                if arg[0] == "--mode":
                    device.set_mode(0 if arg[1] == "auto" else 1, 0)
                elif arg[0] == "--temp":
                    device.set_temp(float(arg[1]))
                elif arg[0] == "--power":
                    device.set_power(0 if arg[1] == "off" else 1, 0)
            print device.type
        else:
            print "error: could not auth"
    print "done"
    return

main()
