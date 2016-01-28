import sys
import re
sys.path.append('./tagger')
import NLPlib
from HTMLParser import HTMLParser

INDEX_TWEET_TEXT = 5

def read_file(file_name):
    """(str of file name) ->Table
    Input a string which is the file name of a table
    """
    file = open(file_name, 'r')
    # read table to get all of the content of the table
    file_list = file.readlines()
    file.close()
    return file_list

def extractTweetText(line):
    line_list = line.split(',"')
    return line_list[INDEX_TWEET_TEXT][:-2]

def removeHTMLTagAttr(tweetText):
    #TODO - rita
    return

def replaceHTMLChars(tweetText):
    parser = HTMLParser()
    return parser.unescape(tweetText)

def removeURL(tweetText):
    #TODO - rita
    return

def removeFirstCharOfUserNameHashTag(tweetText):
    return re.sub(r"[@|#](\w+)", r"\1", tweetText)

def findLineEnding(tweetText):
    #TODO - rita
    return

def getTokenList(tweetText):
    #TODO
    return

def addTagToToken(token):
    #TODO - rita
    return

def addDemarcation(line):
    #TODO
    return

if __name__ == "__main__":
    lst1 = read_file("tweets/testdata.manual.2009.06.14.csv")
    for line in lst1:
        print (removeFirstCharOfUserNameHashTag(replaceHTMLChars(extractTweetText(line))))