#! /usr/bin/env python

import os
import sys
import time
import datetime
from os import listdir
from os.path import isfile, join
import syslog

SYSTEMD_NAME = "seagate"
SERVICE_MODE = 1

DATE_FORMAT = "%d-%m-%Y_%H:%M:%S.tar.gz"
DATE = datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
DATE_NOW = datetime.datetime.now()
BACKUP_THRESHOLD = 3
MOUNT_TIME = 7

EXCLUDES = ['.*', 'Downloads', 'ISOs', 'vmware', 'VMWare', 'Matlab', 'deja-dup', 'snap', 'arduino-*', 'eagle-*']

USERNAME = "brenden"
MOUNT_POINT = "/media/%s/Linux" % USERNAME
HOME_LOC = "/home/%s/" % USERNAME
BACKUP_LOC = "%s/backups/%s/" %(MOUNT_POINT, USERNAME)
BACKUP_LOC_DIR = "%s/backups/%s" %(MOUNT_POINT, USERNAME)
BACKUP_LOC_TAR = "%s/backups/%s.tar.gz" %(MOUNT_POINT, DATE)
OLD_TARS = "%s/backups/" %(MOUNT_POINT)

PROG_RM = "/bin/rm"
PROG_TAR = "/bin/tar"
PROG_RSYNC = "/usr/bin/rsync"
PROG_MKDIR = "/bin/mkdir"
RM_OPTIONS = "-f"
RM_DIR_OPTIONS = "-rf"
TAR_OPTIONS = "-zcvf"
RSYNC_OPTIONS = "-avzh"
MKDIR_OPTIONS = "-p"

START_NOTIFY = '/usr/bin/notify-send -i /usr/local/share/icons/start_backup.png "Starting backup to SSD!"'
SUCCESS_NOTIFY = '/usr/bin/notify-send -i /usr/local/share/icons/success.png "Successfully backed up to SSD!"'
FAIL_NOTIFY = '/usr/bin/notify-send -i /usr/local/share/icons/fail.png "Failed backed up to SSD!\n%s"'
INFO_NOTIFY = '/usr/bin/notify-send -i /usr/local/share/icons/start_backup.png "%s"'

for el in EXCLUDES:
    RSYNC_OPTIONS += " --exclude '%s'" % el

# Logs error to syslog or stdout, depending on SERVICE_MODE variable
def log_error(err):
    if SERVICE_MODE:
        syslog.syslog(syslog.LOG_ERR, err)
    else:
        print FAIL + err + ENDC
    return

# Logs info to syslog or stdout, depending on SERVICE_MODE variable
def log_info(inf):
    if SERVICE_MODE:
        syslog.syslog(syslog.LOG_INFO, inf)
    else:
        print inf
        return

# Main Function
def main():

    if (os.path.isdir(MOUNT_POINT)):
        info = "Found Volume. Starting to sync home directory."
        log_info(info)

        back_files = [f for f in listdir(OLD_TARS) if isfile(join(OLD_TARS, f))]

        for el in back_files:
            temp_date = datetime.datetime.strptime(el, DATE_FORMAT)
            if ((DATE_NOW - temp_date).days < BACKUP_THRESHOLD):
                info = "Last Backup was less than %s days ago. Aborting." % BACKUP_THRESHOLD
                log_info(info)
                os.system(INFO_NOTIFY % info)
                return 0

        if (not os.path.isdir(BACKUP_LOC)):
            print "Creating backup directory: %s" % BACKUP_LOC
            os.system("%s %s %s" %(PROG_MKDIR, MKDIR_OPTIONS, BACKUP_LOC))

        os.system(START_NOTIFY)
        print "Running: %s %s %s %s" %(PROG_RSYNC, RSYNC_OPTIONS, HOME_LOC, BACKUP_LOC)
        ret = os.system("%s %s %s %s > /dev/null" %(PROG_RSYNC, RSYNC_OPTIONS, HOME_LOC, BACKUP_LOC))
        if (ret):
            info = "Couldn't rsync home directory. Aborting"
            log_error(info)
            os.system(FAIL_NOTIFY % info)
            return 1

        print "Running: %s %s %s %s" %(PROG_TAR, TAR_OPTIONS, BACKUP_LOC_TAR, BACKUP_LOC)
        ret = os.system("%s %s %s %s > /dev/null" %(PROG_TAR, TAR_OPTIONS, BACKUP_LOC_TAR, BACKUP_LOC))
        if (ret):
            info = "Couldn't tar backup. Aborting"
            log_error(info)
            os.system(FAIL_NOTIFY % info)
            return 1

        print "Deleting rsync folder: %s" % BACKUP_LOC
        ret = os.system("%s %s %s > /dev/null" %(PROG_RM, RM_DIR_OPTIONS, BACKUP_LOC_DIR))
        if (ret):
            info = "Couldn't remove backup folder. Aborting"
            log_error(info)
            os.system(FAIL_NOTIFY % info)
            return 1

        info = "Done!"
        log_info(info)
        os.system(SUCCESS_NOTIFY)

    else:
        info = "Volume is not mounted. Cannot sync home directory. Aborting"
        log_info(info)
        os.system(FAIL_NOTIFY % info)

    return 0


#############################
if __name__ == "__main__":
    syslog.openlog(SYSTEMD_NAME)
    ret = main()
    syslog.closelog()
    sys.exit(ret)
#############################
