#! /usr/bin/env python2.7

import os
import sys
import requests
import mimetypes
import email
import email.mime.application
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import urllib3
import smtplib
import imaplib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ORG_EMAIL   = "@bicknertrucking.com"
FROM_EMAIL  = "fuel" + ORG_EMAIL
FROM_PWD    = "bicktruck2018!"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

LOGIN_URL = "https://agtracker.nutrien.com/AgTracker/login.jsp"
RES_URL = "https://agtracker.nutrien.com/AgTracker/secure/searchCarrierReleases_results.jsp?carrierNumber=0000100957&searchBy=unshipped&startDate=%s&endDate=%s&origin=ALL&_=1556391958718"
AUTH_URL = "https://agtracker.nutrien.com/AgTracker/Authentication"

DATA = {
    "userid" : "jbickner",
    "pwd" : "#Zkh3352010",
}

ADMIN_EMAIL_LIST = ['john@bicknertrucking.com', 'brenden.j.bickner@gmail.com']
#ADMIN_EMAIL_LIST = ['brenden.j.bickner@gmail.com']

######################################################################
    # Method for sending emails
######################################################################

def send_admin_email():
    # Create a text/plain message
    now = datetime.now()
    the_date = now.strftime("%Y-%m-%d %H:%M:%S")

    msg = email.mime.Multipart.MIMEMultipart()
    msg['Subject'] = 'Nutrien Update Alert ' + the_date
    msg['From'] = FROM_EMAIL
    msg['To'] = FROM_EMAIL

    # The main body is just another attachment
    body = email.mime.Text.MIMEText("""Please see https://agtracker.nutrien.com/AgTracker/secure/searchCarrierReleases.jsp for updates.\n
    Please do not reply, this was an automated message. New emails are sent anytime Nurtien portal is updated.\n
    Report any errors to Brenden Bickner <brenden.j.bickner@gmail.com>""")
    msg.attach(body)

    s = smtplib.SMTP('smtp.gmail.com',port=587)
    s.starttls()
    s.login(FROM_EMAIL,FROM_PWD)
    s.sendmail(FROM_EMAIL, ADMIN_EMAIL_LIST, msg.as_string())
    	
    s.quit()

    return

def get_agtracker():

    release_nums = []

    with requests.Session() as browser:
        res_page = browser.post(AUTH_URL, data=DATA, verify=False)

        # Date Format: Apr+21%2C+2019
        start = (datetime.now() - timedelta(days=6)).strftime("%b+%d+%%2C+%Y")
        end = datetime.now().strftime("%b+%d+%%2C+%Y")

        res_url = RES_URL % (start, end)
        res_page = browser.get(res_url, verify=False)
        
        soup = BeautifulSoup(res_page.text, 'html.parser')
        table_data = soup.find_all('a')
        for el in table_data:
            line = str(el)
            if "releaseDetails" in line:
                temp_soup = BeautifulSoup(line, 'html.parser')
                temp_dat = temp_soup.find_all('a')
                if temp_dat.count > 0:
                    release_nums.append(temp_soup.find_all('a')[0].getText().strip().rstrip())

    write_string = ""
    for el in release_nums:
        write_string += (el + " ")
    write_string += "\n"

    with open('new_release_nums.txt','w') as f:
        f.write(write_string)

    diff = os.system('/usr/bin/diff new_release_nums.txt old_release_nums.txt')

    os.system('/bin/mv new_release_nums.txt old_release_nums.txt')

    if diff:
        msg = "Found new releases! Check Nutrien."
        print msg
        send_admin_email()

    else:
        print "No new releases. Done."

    return

# Main Function
def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print "Starting at: " + now

    get_agtracker()

    return 0


#############################
if __name__ == "__main__":
    sys.exit(main())
#############################
