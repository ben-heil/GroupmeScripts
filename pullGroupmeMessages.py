#!/usr/bin/python

import sys
import json
import requests
import argparse

def chooseGroup(groups):
    print("Here are the groups you are in:")
    print("ID" + "\t\t" + "Group Name")
   
    for i in range(0, len(groups)):
        print((str(i) + "\t" + groups[i]["name"]))
        #TODO: learn how to encode to make things not break
    print()
    print("Type the ID of the group you'd like to download messages from")
    choice = int(input().strip())
    return groups[choice]["group_id"]

def getLatestMessage(groupId, token):
    response = requests.get("https://api.groupme.com/v3/groups/" + groupId +
                          "?token=" + token)
    rawJson = response.json()
    group = rawJson["response"]
    #TODO consider making this a one liner
    
    return group["messages"]["last_message_id"]

def main():
    #Use argparse to take in the user's API token from command line
    parser = argparse.ArgumentParser(description="add flavor text here")
    parser.add_argument("token", help="Your GroupMe API token (go to " +
                        "dev.groupme.com for information on how to get one")
    parser.add_argument("--outFile", default="out.txt", help="Results go here")
    parser.add_argument("--messageID", help="The program will search for message" + 
                        "before this ID")
    parser.add_argument("--groupID", help="This specifies the group from which to" +
                        " pull messages")
    args = parser.parse_args()
    
    baseURL = "https://api.groupme.com/v3"
    
    #Retrieve and parse the response
    groupResponse = requests.get(baseURL + "/groups?per_page=10&token=" + args.token)
    
    try:
        outFile = open(args.outFile, 'w')
    except IOError:
        print("The file didn't open")
        exit(1)
    
    jsonDict = groupResponse.json()
    
    firstMessage = args.messageID
    chosenGroup = args.groupID
    
    if chosenGroup == None:
        chosenGroup = chooseGroup(jsonDict["response"])

    if firstMessage == None:
        firstMessage = getLatestMessage(chosenGroup, args.token)
    print(chosenGroup)
    
    
    #TODO: get first message
    
    status = "200"
    
    while(status == "200"):
        pass
    
    #Have to encode the string before writing 
    outFile.write(str(groupResponse.text.encode('utf-8')))
    
    #print("Input the ID of the group which you would like to download messages from)
    #
    #groupID = str(sys.stdin.read())
    #
    #urlExtension = "/groups/" + groupId + "/messages?" + args.token
    #
    #print(baseURL + urlExtension)
    #

if __name__ == "__main__":
   exit (main())