import sys
import re
import NLPlib
from HTMLParser import HTMLParser

reload(sys)
sys.setdefaultencoding("latin-1")
INDEX_TWEET_TEXT = 5
INDEX_DEMARCATION = 0

ABBREV_FILES_PATH = '/u/cs401/Wordlists/'
ABBREV_FILES = ['abbrev.english', 'pn_abbrev.english', 'pn_abbrev.english2']
SUFFIX_ABBREV = '_DOT'

def read_file(file_name):
    '''
    Read a file with given file name and return all lines in that file.
    '''
    file = open(file_name, 'r')
    lines = file.readlines()
    file.close()
    return lines

def extractTweetText(line):
    '''
    Extract the tweet text from a given line.
    '''
    line_list = line.split(',"')
    return line_list[INDEX_TWEET_TEXT].strip()[:-1].strip()

def removeHTMLTagAttr(sentence):
    '''
    Remove all HTML tags and attributes in the given sentence.
    '''
    return re.sub('<[^<]+?>', '', sentence)

def replaceHTMLChars(sentence):
    '''
    Replace all HTML characters in the given sentence.
    '''
    parser = HTMLParser()
    return parser.unescape(sentence)

def removeURL(sentence):
    '''
    Remove URL's in the given sentence.
    '''
    return re.sub(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)", "", sentence)

def removeFirstCharOfUserNameHashTag(sentence):
    '''
    Remove first character of user name and hash tag.
    '''
    return re.sub(r"[@|#](\w+)", r"\1", sentence)

def getSentences(tweetText):
    '''
    Return a list of sentences given the tweet text.
    '''
    return re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s?', tweetText)

def decorateAbbrev(tweetText):
    '''
    Replace '.' in abbreviations with '_DOT'. 
    '''
    for abbrevFilePath in ABBREV_FILES:
        # Read the abbreviation file
        abbrevFile = open(ABBREV_FILES_PATH + abbrevFilePath, 'r')
        for line in abbrevFile.readlines():
            line = line.strip()
            tweetText = tweetText.replace(' ' + line, ' ' + line[:-1] + '_DOT')

    return tweetText

def getTokenTagList(nlp, sentence):
    '''
    Return the token/tag list from a given sentence.
    '''
    it = re.finditer(r"\w+|'\w+|[^\w\s]+", sentence)
    tokens = []
    for match in it:
        # Put the '.' back for each occurence of '_DOT'
        tokens.append(match.group().replace(SUFFIX_ABBREV, '.'))

    nlpRes = nlp.tag(tokens)
    res = []
    for i in range(len(tokens)):
        # Build the token/tag pair
        comb = tokens[i] + '/' + nlpRes[i]
        res.append(comb)
    return res

def getDemarcation(line):
    '''
    Get the demarcation from a given line.
    '''
    line_list = line.split(',"')
    return "<A=" + line_list[INDEX_DEMARCATION][1] +">"

if __name__ == "__main__":
    inputFile = ''
    outputFile = ''
    groupNumber = None

    # Read command line inputs first
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

    # Extract the training data using given group number
    trainingData = []
    if groupNumber:
        trainingData = lines[groupNumber * 5500: (groupNumber + 1) * 5500] + lines[800000 + groupNumber * 5500: 800000 + (groupNumber + 1) * 5500]
    else:
        trainingData = lines

    resFile = open(outputFile, "w")
    nlp = NLPlib.NLPlib()
    for line in trainingData:
        # Parse each line in the training data and build the token/tag pairs
        resFile.write(getDemarcation(line))
        resFile.write("\n")
        tweetText = extractTweetText(line)
        tweetText = decorateAbbrev(tweetText)
        for sentence in getSentences(tweetText):
            # Process each sentence from each line
            sentence = removeURL(sentence)
            sentence = replaceHTMLChars(sentence)
            sentence = removeFirstCharOfUserNameHashTag(sentence)
            sentence = removeHTMLTagAttr(sentence)
            sentence = sentence.strip()

            tokenTagList = getTokenTagList(nlp, sentence)
            # Write the result into the output file
            for tokenTag in tokenTagList:
                resFile.write(tokenTag + " ")
            resFile.write("\n")
