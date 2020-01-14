#! /usr/bin/env python3

# Configuration
# TODO: move to /etc/
SERVICES = {
    "vanilluxe": 25567,
    "nginx": 80,
    "deadtest": 69,
}
PATH = "/var/lib/service-stat"

import subprocess
import os
import sys
import errno
import time
import json


def is_up(port):
    return int(subprocess.check_output(
        "lsof -i:{} -Pn | grep LISTEN | wc -l".format(
            port
        ),
        shell=True,
    ).strip()) > 0


def write_status(service, status):
    filename = os.path.join(PATH, service)
    line = (
        ("1:" if status else "0:")
        + str(time.time()) + "\n"
    )
    with open(filename, "a+") as service_file:
        service_file.write(line)


def get_system_uptime():
    # TODO
    return 1.0


def get_uptime(service, period=1*60*60*24):
    filename = os.path.join(PATH, service)
    with open(filename, "r") as service_file:
        up = 0
        down = 0
        for line in service_file:
            status, ts = line.strip().split(":") 
            if float(time.time() - period) > float(ts):
                continue

            if int(status):
                up += 1
            else:
                down += 1 
    try:
        return down / up if down != 0 else 1.0
    except ZeroDivisionError:
        return 0.0
        

def main():
    permission_err = "You need to be root to run this!"
    no_lsof_err = "This program needs 'lsof' to be installed!"

    status = {
        "service": {},
        "system": {},
    }

    if not os.path.exists(PATH):
        try:
            os.mkdir(PATH)
        except IOError:
            print(json.dumps({"error":permission_err}))
            sys.exit(errno.EACCES)

    for name, port in SERVICES.items():
        try:
            service_status = is_up(port)
        except OSError:
            print(json.dumps({"error":no_lsof_err}))
            sys.exit(errno.ENOPKG)
        try:
            write_status(name, service_status)
        except IOError:
            print(json.dumps({"error":permission_err}))
            sys.exit(errno.EACCES)

        raw_uptime = get_uptime(name)
        uptime = raw_uptime * get_system_uptime()

        status['service'][name] = {
            "status": int(service_status),
            "uptime": uptime,
            "raw_uptime": uptime,
        }
    print(json.dumps(status))


if __name__ == "__main__":
    if sys.platform != "linux":
        print("This program only supports Linux systems!")
    main()

