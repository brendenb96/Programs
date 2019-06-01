#! /usr/bin/env python

import os
import sys
import subprocess
import colored

SEARCHDIRS = ["/home/brenden" ,"/usr/local/src"]
SEARCHKEY = ".git"
IGNORE = ["multi-monitors-add-on"]

REMOTE_STAT_COMMAND = "cd %s && git fetch --dry-run"
LOCAL_STAT_COMMAND = "cd %s && git status"

# Main Function
def main():

    git_repos = []

    for search_dir in SEARCHDIRS:
        for root, dirs, files in os.walk(search_dir):
            for look_dir in dirs:
                if SEARCHKEY == look_dir:
                    for el in IGNORE:
                        if el not in root:
                            git_repos.append(root)

    for git_repo in git_repos:
        print "Checking: %s" % git_repo
        out = subprocess.check_output(REMOTE_STAT_COMMAND % git_repo, stderr=subprocess.STDOUT, shell=True)
        if out != "":
            print "%s out of sync with remote." % git_repo
        out = subprocess.check_output(LOCAL_STAT_COMMAND % git_repo, stderr=subprocess.STDOUT, shell=True)
        local = False

        for line in out.split("\n"):
            if "Changes to be committed" in line:
                local = True
            if "Changes not staged for commit" in line:
                local = True
            if ""

    return 0


#############################
if __name__ == "__main__":
    sys.exit(main())
#############################
