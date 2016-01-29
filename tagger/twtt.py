import sys
import re
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
    return re.sub(r"(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?", "", tweetText)


def removeFirstCharOfUserNameHashTag(tweetText):
    return re.sub(r"[@|#](\w+)", r"\1", tweetText)

def getSentences(tweetText):
    return re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', tweetText)

def getTokenTagList(tweetText):
    it = re.finditer(r"\w+|'\w+|[^\w\s]+", tweetText)
    tokens = []
    for match in it:
        tokens.append(match.group())
    nlp = NLPlib.NLPlib()
    nlpRes = nlp.tag(tokens)
    res = []
    for i in range(len(tokens)):
        comb = tokens[i] + '/' + nlpRes[i]
        res.append(comb)

    return res

def addDemarcation(line):
    #TODO
    return

if __name__ == "__main__":
    o = NLPlib.NLPlib()
    lst1 = read_file("../tweets/testdata.manual.2009.06.14.csv")
    for line in lst1:

        a = getTokenTagList(extractTweetText(line))
        print (a)