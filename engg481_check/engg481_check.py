#! /usr/bin/env python

import sys
import requests
import datetime
from twilio.rest import Client

LINKS = ["http://contacts.ucalgary.ca/info/enel/courses/w19/ENGG481"]
SEARCH_KEYS = ["Spring 2019","Summer 2019"]

TARGET_PHONE = "+13067417636"
FROM_PHONE = "+13067003527"

SID = "ACdb1cfa0b3d09eef6ad7c768f45f22112"
TOKEN = "a6683b8e4f07db3507494ff740abe5cb"

# Main Function
def main():
    now = datetime.datetime.now()
    the_date = now.strftime("%Y-%m-%d %H:%M:%S")
    print "Starting check at " + the_date

    for link in LINKS:
        page = requests.get(link)
        data = page.text
        data = data.split("\n")
        target_class = link.split("/")[-1]
        
        found = False
        for line in data:
            for key in SEARCH_KEYS:
                if key in line:
                    found = True;

        if found:
            print target_class + " is now available! Sending text."
            try:
                client = Client(SID, TOKEN)
                client.messages.create(to=TARGET_PHONE, from_=FROM_PHONE, body= target_class + " is now available! Sign up now.")
            except Exception as e:
                print "Error Sending: " + str(e)
        else:
            print target_class + " is not available yet."

    return 0

# Entry Point
#############################
if __name__ == "__main__":
    sys.exit(main())
#############################