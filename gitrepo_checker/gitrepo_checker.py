#! /usr/bin/env python

import os
import sys
import getpass
import subprocess
from optparse import OptionParser
from datetime import datetime

try:
    from termcolor import colored, cprint
    from tabulate import tabulate
except Exception:
    print 'Missing packages. run "sudo make packages" first!'
    sys.exit(1)

SEARCHDIRS = ["/home/%s" % getpass.getuser() ,"/usr/local/src"]
SEARCHKEY = ".git"
IGNORE = ["multi-monitors-add-on"]

REMOTE_STAT_COMMAND = "cd %s && git fetch --dry-run"
LOCAL_STAT_COMMAND = "cd %s && git status"
CRED_STORE_COMMAND = "cd %s && git config credential.helper store"

TYPES = ["plain", "simple", "github", "grid", "fancy_grid", "pipe", "orgtbl", "jira", "presto", "psql", "rst", "mediawiki", 
            "moinmoin", "youtrack", "html", "latex", "latex_raw", "latex_booktabs", "textile"]

HEAD_ATTRS = ["bold", "underline"]

ALIGN = ["left", "center", "center", "center"]
VERBOSE_ALIGN = ["left", "center", "center", "center" , "center" , "center"]

# Main Function
def main():

    usage = "git-check [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="prints details of repos")
    parser.add_option("-c", "--credentials", action="store_true", dest="credentials", help="allows repos to store credentials")
    parser.add_option("-p", "--prompt-credentials", action="store_true", dest="prompt-credentials", help="prompts user for credentials at start of program")
    (options, args) = parser.parse_args()
    verbose = options.verbose
    credentials = options.credentials

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
        temp_values = []
        temp_values.append(colored(git_repo, 'white'))

        local = False
        remote = False
        not_commited = False
        not_staged = False
        branch_ahead = False
        untracked = False

        if credentials:
            subprocess.check_output(CRED_STORE_COMMAND % git_repo, stderr=subprocess.STDOUT, shell=True)

        try:
            out = subprocess.check_output(REMOTE_STAT_COMMAND % git_repo, stderr=subprocess.STDOUT, shell=True)
        except KeyboardInterrupt:
            print colored("\nIf you are being asked to submit credentials, try running program with -c option\nThis will prompt once for each git repo then store credentials after.", 'green')
            return 1

        if out != "":
            remote = True
        
        out = subprocess.check_output(LOCAL_STAT_COMMAND % git_repo, stderr=subprocess.STDOUT, shell=True)
        for line in out.split("\n"):
            if "Changes to be committed" in line:
                local = True
                not_commited = True
            if "Changes not staged for commit" in line:
                local = True
                not_staged = True
            if "Your branch is ahead" in line:
                local = True
                branch_ahead = True
            if "Untracked files" in line:
                local = True
                untracked = True

        if local:
            temp_issues = ""
            if verbose:
                if not_commited:
                    temp_issues += colored("Uncommitted changes",'red') + "\n"
                if not_staged:
                    temp_issues += colored("Unstaged changes",'red') + "\n"
                if branch_ahead:
                    temp_issues += colored("Unpushed committs",'red') + "\n"
                if untracked:
                    temp_issues += colored("Untracked files",'red') + "\n"
                temp_values.append(temp_issues)

            else:
                temp_values.append(colored(u'\u2717', 'red'))

        else:
            if verbose:
                temp_values.append(colored("All Good!", 'green'))
            else:
                temp_values.append(colored(u'\u2713', 'green'))

        if remote:
            if verbose:
                temp_values.append(colored("Unpulled changes on remote", 'red'))
            else:
                temp_values.append(colored(u'\u2717', 'red'))
        else:
            if verbose:
                temp_values.append(colored("All Good!", 'green'))
            else:
                temp_values.append(colored(u'\u2713', 'green'))

        if verbose:
            try:
                temp_values.append(datetime.utcfromtimestamp(os.path.getmtime("%s/.git/FETCH_HEAD" % git_repo)).strftime('%Y-%m-%d %H:%M:%S'))
            except Exception:
                try:
                    temp_values.append(datetime.utcfromtimestamp(os.path.getmtime("%s/.git/HEAD" % git_repo)).strftime('%Y-%m-%d %H:%M:%S'))
                except Exception:
                    temp_values.append(colored("Coudln't find last pull time", 'red'))

            try:
                temp_values.append(datetime.utcfromtimestamp(os.path.getmtime(git_repo)).strftime('%Y-%m-%d %H:%M:%S'))
            except Exception:
                temp_values.append(colored("Coudln't get last mod time", 'red'))

        if remote or local:
            up_to_date = False
            if verbose:
                temp_values.append(colored("Not up to date!", 'red'))
            else:
                temp_values.append(colored(u'\u2717', 'red'))
        else:
            if verbose:
                temp_values.append(colored("Up to date!", 'green'))
            else:
                temp_values.append(colored(u'\u2713', 'green'))


        values.append(temp_values)

    if verbose:
        headers = [colored("Repository", 'white', attrs=HEAD_ATTRS), colored("Local Status", 'white', attrs=HEAD_ATTRS), 
                    colored("Remote Status", 'white', attrs=HEAD_ATTRS), colored("Last Pull", 'white', attrs=HEAD_ATTRS),
                    colored("Last Mod", 'white', attrs=HEAD_ATTRS), colored("Overall", 'white', attrs=HEAD_ATTRS)]
        print tabulate(values, headers, tablefmt='fancy_grid', colalign=VERBOSE_ALIGN)

    else:
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
