#!/usr/bin/env python

import argparse
from itertools import zip_longest
import sys
import operator

class PostCounter:
        def __init__(self):
            self.idToAuthor = dict()
            self.postCount = dict()
            
        def countPost(self, id, name):
            if id in self.idToAuthor:
                self.postCount[id] = self.postCount[id] + 1
            else:
                self.idToAuthor[id] = name
                self.postCount[id] = 1
    
        def printPostCounts(self):
            countIterator = sorted(self.postCount.items(), 
			    key=operator.itemgetter(1), reverse=True)
            for count in countIterator:
                print("{0: <40}".format(self.idToAuthor[count[0]]) + str(count[1])) 
	

def main():
    parser = argparse.ArgumentParser(description="Reads in output from " +
        "downloadGroupmeMessages and counts the posts from each user")
    parser.add_argument("inFile", help="The file containing the stored messages")
    parser.add_argument("--outFile", default="out.txt", help="Results go here")
    args = parser.parse_args()

    with open(args.inFile, 'r') as infile:
        
        counter = PostCounter()
        
	#Throw away header
        infile.readline()
        for line in infile:
            line = line.split("\t")
            name = line[1]
            ID = line[0]
            counter.countPost(ID, name)

        counter.printPostCounts()

if __name__ == "__main__":
   exit(main())
