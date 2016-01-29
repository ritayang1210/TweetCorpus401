import sys
import re
import NLPlib
from HTMLParser import HTMLParser

INDEX_TWEET_TEXT = 5
INDEX_DEMARCATION = 0

def read_file(file_name):
    """(str of file name) ->Table
    Input a string which is the file name of a table
    """
    file = open(file_name, 'r')
    # read table to get all of the content of the table
    lines = file.readlines()
    file.close()
    return lines

def extractTweetText(line):
    line_list = line.split(',"')
    return line_list[INDEX_TWEET_TEXT][:-2]

def removeHTMLTagAttr(sentence):
    return re.sub('<[^<]+?>', '', sentence)

def replaceHTMLChars(sentence):
    parser = HTMLParser()
    return parser.unescape(sentence)

def removeURL(sentence):
    return re.sub(r"(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?", "", sentence)

def removeFirstCharOfUserNameHashTag(sentence):
    return re.sub(r"[@|#](\w+)", r"\1", sentence)

def getSentences(tweetText):
    return re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', tweetText)

def getTokenTagList(nlp, sentence):
    it = re.finditer(r"\w+|'\w+|[^\w\s]+", sentence)
    tokens = []
    for match in it:
        tokens.append(match.group())
    
    nlpRes = nlp.tag(tokens)
    res = []
    for i in range(len(tokens)):
        comb = tokens[i] + '/' + nlpRes[i]
        res.append(comb)
    return res

def getDemarcation(line):
    line_list = line.split(',"')
    return "<A=" + line_list[INDEX_DEMARCATION][1] +">"

if __name__ == "__main__":
    nlp = NLPlib.NLPlib()
    lines = read_file("../tweets/testdata.manual.2009.06.14.csv")
    for line in lines:
        print getDemarcation(line)
        tweetText = extractTweetText(line)
        for sentence in getSentences(tweetText):
            sentence = removeURL(sentence)
            sentence = replaceHTMLChars(sentence)
            sentence = removeFirstCharOfUserNameHashTag(sentence)
            sentence = removeHTMLTagAttr(sentence)

            tokenTagList = getTokenTagList(nlp, sentence)
            for tokenTag in tokenTagList:
                print tokenTag,
            print





    # a = getTokenTagList(extractTweetText(line))
        # print (a)