import sys
import re
import NLPlib
from HTMLParser import HTMLParser

reload(sys)
sys.setdefaultencoding("latin-1")
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
    return re.sub(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)", "", sentence)

def removeFirstCharOfUserNameHashTag(sentence):
    return re.sub(r"[@|#](\w+)", r"\1", sentence)

def getSentences(tweetText):
    return re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s?', tweetText)

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
    inputFile = ''
    outputFile = ''
    groupNumber = None
    if len(sys.argv) == 3:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]
    elif len(sys.argv) == 4:
        inputFile = sys.argv[1]
        groupNumber = int(sys.argv[2])
        outputFile = sys.argv[3]
    else:
        print 'usage: twtt.py <inputFile> [<groupNumber>] <outputFile>'
        sys.exit()

    lines = read_file(inputFile)

    trainingData = []
    if groupNumber:
        trainingData = lines[groupNumber * 5500: (groupNumber + 1) * 5500] + lines[800000 + groupNumber * 5500: 800000 + (groupNumber + 1) * 5500]
    else:
        trainingData = lines

    resFile = open(outputFile, "w")
    nlp = NLPlib.NLPlib()
    for line in trainingData:
        resFile.write(getDemarcation(line))
        resFile.write("\n")
        tweetText = extractTweetText(line)
        for sentence in getSentences(tweetText):
            sentence = removeURL(sentence)
            sentence = replaceHTMLChars(sentence)
            sentence = removeFirstCharOfUserNameHashTag(sentence)
            sentence = removeHTMLTagAttr(sentence)
            sentence = sentence.strip()

            if not sentence:
                continue

            tokenTagList = getTokenTagList(nlp, sentence)
            for tokenTag in tokenTagList:
                resFile.write(tokenTag + " ")
            resFile.write("\n")
