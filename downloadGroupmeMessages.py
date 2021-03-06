#!/usr/bin/python

import sys
import json
import requests
import argparse


def asciiWrite(outFile, message):
    outFile.write(message.encode(encoding ='ascii', errors = 'ignore'))

#This function strips emojii and other characters that can't be written to a txt file
def asciiPrint(message):
    sys.stdout.write(str((message.encode(encoding ='ascii', errors = 'ignore'))))

def chooseGroup(groups):
    print("Here are the groups you are in:")
    print("ID" + "    " + "Group Name")
   
    i = 0
    for group in groups:
        groupLabel = str(i) + "    " + groups[i]["name"]
        asciiPrint(groupLabel)
        print()
        i += 1
    print()
    print("Type the number of the group you'd like to download messages from")
    choice = int(input().strip())
    return groups[choice]["group_id"]

def getLatestMessage(groupId, token):
    response = requests.get("https://api.groupme.com/v3/groups/" + groupId +
                          "?token=" + token)
    rawJson = response.json()
    group = rawJson["response"]
    return group["messages"]["last_message_id"]

def recordMessages(rawResponse, currentMessage, outFile):
        messageResponse = rawResponse.json()
        
        messages = messageResponse["response"]["messages"]
        for message in messages:
            currentMessage = message["id"]

            id = str(message["user_id"] + "\t")
            asciiWrite(outFile, id)
            
            name = str(message["name"] + "\t")
            asciiWrite(outFile, name)
            
            time = str(message["created_at"]) + "\t"
            asciiWrite(outFile, time)
            
            if message["text"] is None:
                asciiWrite(outFile, "Picture\t")
            else:
                text = str(message["text"] + "\t")
                asciiWrite(outFile, text.replace("\n", " - "))
            if not message["favorited_by"]:
                asciiWrite(outFile, "No favorites")
            for favorite in message["favorited_by"]:
                favorite = favorite + ";"
                asciiWrite(outFile, favorite)
            asciiWrite(outFile,"\t")
            favoriteCount = str(len(message["favorited_by"])) + "\t"
            asciiWrite(outFile, favoriteCount)
            asciiWrite(outFile, "\r\n")
            
        return currentMessage

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
    
    groupResponse = requests.get(baseURL + "/groups?per_page=100&token=" + args.token)
    
    try:
        outFile = open(args.outFile, 'ab')
    except IOError:
        print("The file didn't open")
        exit(1)
    
    jsonDict = groupResponse.json()
    
    currentMessage = args.messageID
    chosenGroup = args.groupID
    token = args.token
    
    if chosenGroup == None:
        chosenGroup = chooseGroup(jsonDict["response"])
        asciiWrite(outFile, "UserID\tName\tTime\tMessage\tFavorites\tFavoriteCount\t\r\n")

    if currentMessage == None:
        currentMessage = getLatestMessage(chosenGroup, args.token)
    
    #Used for a DIY do-while loop
    responseIsGood = True
    
    messagesRead = 0
    while responseIsGood:
        rawResponse = requests.get("https://api.groupme.com/v3/groups/" +
                                           chosenGroup + "/messages?token=" + token +
                                           "&limit=100&before_id="+currentMessage)
    
        responseIsGood = rawResponse.status_code == 200
        
        if responseIsGood:         
            messagesRead += 100
            print(str(messagesRead) + " messages recorded")
            currentMessage = recordMessages(rawResponse, currentMessage, outFile)
        else:
            if rawResponse.status_code == 304:
                print("All messages downloaded")
            elif rawResponse.status_code == 420:
                print("Rate limit exceeded, try again later, specifying " +
                      "messageID " + currentMessage + "\n and groupID " 
                      + chosenGroup + " as parameters")
            else: 
                print("Error: " + str(rawResponse.status_code))     

if __name__ == "__main__":
   exit (main())
