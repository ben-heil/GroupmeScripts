import sys
import argparse
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

#Makes a leaderboard of people with the most negative and most positive posts
#By using the vader sentiment intensity analyzer from the nltk

class PostSentimentCounter:
        def __init__(self):
            self.idToAuthor = {}
            self.idToCount = {}
            self.idToPosSentiment = {}
            self.idToNegSentiment = {}
            
        def countPost(self, id, name, sentimentDictionary):
            if id in self.idToAuthor:
                self.idToCount[id] += 1
                self.idToPosSentiment[id] += sentimentDictionary['pos']
                self.idToNegSentiment[id] += sentimentDictionary['neg']
            else:
                self.idToAuthor[id] = name
                self.idToCount[id] = 1
                self.idToNegSentiment[id] = sentimentDictionary['neg']
                self.idToPosSentiment[id] = sentimentDictionary['pos']
    
        def printSentimentLeaderboards(self):
            posSentimentList = []
            negSentimentList = []
            #Create list of averaged sentiments, sort, and print
            for key in self.idToPosSentiment:
                if(self.idToCount[key] > 100):
                    self.idToPosSentiment[key] /= self.idToCount[key]
                    posSentimentList.append((self.idToPosSentiment[key], self.idToAuthor[key]))
                    self.idToNegSentiment[key] /= self.idToCount[key]
                    negSentimentList.append((self.idToNegSentiment[key], self.idToAuthor[key]))
            print("Negative sentiment leaderboard")
            for item in reversed(sorted(negSentimentList)):
                print(item)
            print("\nPositive sentiment leaderboard")
            for item in reversed(sorted(posSentimentList)):
                print(item)
            
def main():
    parser = argparse.ArgumentParser(description="Reads in output from " +
        "downloadGroupmeMessages and runs a sentiment analysis")
    parser.add_argument("inFile", help="The file containing the stored messages")
    parser.add_argument("--outFile", default="out.txt", help="Results go here")
    args = parser.parse_args()
    
    print("\nThis program prints the most negative and positive users of the chat ranked according to their average score from the VADER sentiment intensity analyzer in the NLTK. Not super accurate, but it's a fun conversation starter")
    print("The program takes a few seconds to run, and requires that you have some of the NLTK corpora installed.")

    with open(args.inFile, 'r') as infile:
        infile.readline()
        analyzer = SentimentIntensityAnalyzer()
        negList = []
        positiveList = []
        counter = PostSentimentCounter()
        for line in infile:
            line = line.split('\t')
            message = line[3]
            id = line[0]
            name = line[1]
            
            sentDict = analyzer.polarity_scores(message)
            counter.countPost(id, name, sentDict)
        counter.printSentimentLeaderboards()
         
        

if __name__ == '__main__':
    sys.exit(main())
