#!/Python34/python.exe

import sys
import json
import requests

#Take in the API token as a command line parameter
token = sys.argv[1:]
groupId = sys.argv[2:]

baseURL = "https://api.groupme.com/v3"

print(baseURL)
