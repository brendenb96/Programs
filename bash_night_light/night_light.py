#! /usr/bin/env python

import sys
import os
import subprocess

GET_CMD = "/usr/bin/gsettings get org.gnome.settings-daemon.plugins.color night-light-enabled"
ON_CMD = "/usr/bin/gsettings set org.gnome.settings-daemon.plugins.color night-light-enabled true"
OFF_CMD = "/usr/bin/gsettings set org.gnome.settings-daemon.plugins.color night-light-enabled false"

OFF_NOTIFY = '/usr/bin/notify-send -i /usr/local/share/icons/sun.png "Night Mode is off!"'
ON_NOTIFY = '/usr/bin/notify-send -i /usr/local/share/icons/moon.png "Night Mode is on!"'

# Main Function
def main():

    status = subprocess.check_output(GET_CMD, stderr=subprocess.STDOUT, shell=True)
    
    if "true" in status:
        os.system(OFF_CMD)
        os.system(OFF_NOTIFY)
    else:
        os.system(ON_CMD)
        os.system(ON_NOTIFY)

    return 0


#############################
if __name__ == "__main__":
    sys.exit(main())
#############################
