#!/usr/bin/python

import sys
import json
import requests
import argparse

class PostCounter:
        def __init__(self):
            #Note, you need the idToAuthor dictionary because users can change
            #their names
            self.idToAuthor = dict()
            self.postCount = dict()
            
        def countPost(self, post):
            authorId = post["user_id"]
            if authorId in self.idToAuthor:
                self.postCount[authorId] = self.postCount[authorId] + 1
            else:
                self.idToAuthor[authorId] = post["name"]
                self.postCount[authorId] = 1
    
        #TODO: change this to a accessor function of some sort
        def printPostCounts(self):
            for key in self.postCount:
                print(self.idToAuthor[key].encode('utf-8'), "\t", 
                      str(self.postCount[key]).encode('utf-8'))
        
        

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
    
    currentMessage = args.messageID
    chosenGroup = args.groupID
    token = args.token
    
    if chosenGroup == None:
        chosenGroup = chooseGroup(jsonDict["response"])

    if currentMessage == None:
        currentMessage = getLatestMessage(chosenGroup, args.token)
    print(chosenGroup)
    
    
    #TODO: get first message
    
    status = "200"
    
    
    count = PostCounter()
    
    while status == "200":
        messageResponse = requests.get("https://api.groupme.com/v3/groups/" +
                                       chosenGroup + "/messages?token=" + token +
                                       "&limit=100&before_id="+currentMessage)
        messageResponse = messageResponse.json()
        status = messageResponse["meta"]["code"]
        print(status)
        messages = messageResponse["response"]["messages"]
        for message in messages:
            count.countPost(message)
            id = str(message["user_id"] + "\n")
            outFile.write(id.encode('utf-8'))
            name = str(message["name"] + "\n")
            outFile.write(name.encode(encoding='utf_8', errors='ignore'))
            text = str(message["text"] + "\n")
            outFile.write(text.encode(encoding='utf-8', errors='ignore'))
            for favorite in message["favorited_by"]:
                outFile.write(favorite.encode('utf-8') + ", ")
            outFile.write("\n")
            
    count.printPostCounts()    
    
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