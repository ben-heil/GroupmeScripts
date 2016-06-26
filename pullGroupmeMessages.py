#!/usr/bin/python

import sys
import json
import requests
import argparse

#Use argparse to take in the user's API token from command line
parser = argparse.ArgumentParser(description="add flavor text here")
parser.add_argument("token", help="Your GroupMe API token (go to dev.groupme.com for information on how to get one")
parser.add_argument("--outFile", default="out.txt", help="Results go here")

args = parser.parse_args()

baseURL = "https://api.groupme.com/v3"

#Retrieve and parse the response
groupRequest = requests.get(baseURL + "/groups?token=" + args.token)

try:
    outFile = open(args.outFile, 'w')
except IOError:
    print("The file didn't open")
    exit(1)

#Have to encode the string before writing 
outFile.write(str(groupRequest.text.encode('utf-8')))

#print("Input the ID of the group which you would like to download messages from)
#
#groupID = str(sys.stdin.read())
#
#urlExtension = "/groups/" + groupId + "/messages?" + args.token
#
#print(baseURL + urlExtension)
#
