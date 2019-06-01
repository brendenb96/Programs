#! /usr/bin/env python

import os
import sys
import subprocess
from termcolor import colored, cprint
from tabulate import tabulate

SEARCHDIRS = ["/home/brenden" ,"/usr/local/src"]
SEARCHKEY = ".git"
IGNORE = ["multi-monitors-add-on"]

REMOTE_STAT_COMMAND = "cd %s && git fetch --dry-run"
LOCAL_STAT_COMMAND = "cd %s && git status"

TYPES = ["plain", "simple", "github", "grid", "fancy_grid", "pipe", "orgtbl", "jira", "presto", "psql", "rst", "mediawiki", 
            "moinmoin", "youtrack", "html", "latex", "latex_raw", "latex_booktabs", "textile"]

HEAD_ATTRS = ["bold", "underline"]
ALIGN = ["left", "center", "center", "center"]

# Main Function
def main():

    verbose = True

    print colored("Starting Git Repo Checker...\n", 'blue', attrs=['bold'])

    git_repos = []
    values = []
    up_to_date = True

    for search_dir in SEARCHDIRS:
        for root, dirs, files in os.walk(search_dir):
            for look_dir in dirs:
                if SEARCHKEY == look_dir:
                    for el in IGNORE:
                        if el not in root:
                            git_repos.append(root)

    for git_repo in git_repos:
        #print colored("Checking: %s" % git_repo, 'white', attrs=['bold'])
        temp_values = []
        temp_values.append(colored(git_repo, 'white'))
        local = False
        remote = False
        

        out = subprocess.check_output(REMOTE_STAT_COMMAND % git_repo, stderr=subprocess.STDOUT, shell=True)
        if out != "":
            remote = True
        
        out = subprocess.check_output(LOCAL_STAT_COMMAND % git_repo, stderr=subprocess.STDOUT, shell=True)
        for line in out.split("\n"):
            if "Changes to be committed" in line:
                local = True
            if "Changes not staged for commit" in line:
                local = True
            if "Your branch is ahead" in line:
                local = True

        if local:
            if verbose:
            else:
                temp_values.append(colored(u'\u2717', 'red'))
        else:
            temp_values.append(colored(u'\u2713', 'green'))

        if remote:
            if verbose:
            else:
                temp_values.append(colored(u'\u2717', 'red'))
        else:
            if verbose:
            else:
                temp_values.append(colored(u'\u2713', 'green'))

        if remote or local:
            up_to_date = False
            if verbose:
            else:
                temp_values.append(colored(u'\u2717', 'red'))
        else:
            if verbose:
            else:
                temp_values.append(colored(u'\u2713', 'green'))

        values.append(temp_values)

    headers = [colored("Repository", 'white', attrs=HEAD_ATTRS), colored("Local Status", 'white', attrs=HEAD_ATTRS), 
                colored("Remote Status", 'white', attrs=HEAD_ATTRS), colored("Overall", 'white', attrs=HEAD_ATTRS)]

    print tabulate(values, headers, tablefmt='fancy_grid', colalign=ALIGN)
    print ""

    if up_to_date:
        return 0
    else:
        return 1


#############################
if __name__ == "__main__":
    sys.exit(main())
#############################
