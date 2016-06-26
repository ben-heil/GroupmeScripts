#!/usr/bin/python

import sys
import json
import requests
import argparse

#Use argparse to take in the user's API token from command line
parser = argparse.ArgumentParser(description="add flavor text here")
parser.add_argument("token", help="Your GroupMe API token (go to dev.groupme.com for information on how to get one")
args = parser.parse_args()
parser.add_argument("outFile", help="Results go here", default="out.txt")

baseURL = "https://api.groupme.com/v3"

groupRequest = requests.get(baseURL + "/groups?token=" + args.token)

print(groupRequest.encoding)

#print("Input the ID of the group which you would like to download messages from)
#
#groupID = str(sys.stdin.read())
#
#urlExtension = "/groups/" + groupId + "/messages?" + args.token
#
#print(baseURL + urlExtension)
#
