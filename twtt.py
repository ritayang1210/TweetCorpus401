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
    return re.sub('<[^<]+?>', '', tweetText)

def replaceHTMLChars(tweetText):
    parser = HTMLParser()
    return parser.unescape(tweetText)

def removeURL(tweetText):
    return " ".join(filter(lambda x:(x[0:4]!='http' and x[0:3]!='www'), tweetText.split()))


def removeFirstCharOfUserNameHashTag(tweetText):
    return re.sub(r"[@|#](\w+)", r"\1", tweetText)

def findLineEnding(tweetText):
    #TODO - rita
    return

def getTokenList(tweetText):
    it = re.finditer(r"\w+|'\w+|[^\w\s]+", tweetText)
    res = []
    for match in it:
        res.append(match.group())
    return res

def addTagToToken(token):
    #TODO - rita
    return

def addDemarcation(line):
    #TODO
    return

if __name__ == "__main__":
    o = NLPlib.NLPlib()
    lst1 = read_file("tweets/testdata.manual.2009.06.14.csv")
    s = "<head attr= kkkkk's> $25 in he'll </heads> there ... ,,, !!! .' "

    a = getTokenList(s)
    print (a)
    print (o.tag(a))