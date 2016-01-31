import re
import sys

PATH_WORDLISTS = '../Wordlists'

SLANGS = [x.lower() for x in open(PATH_WORDLISTS + '/Slang', 'r').read().splitlines()]
FIRST_PERSON_PRON = [x.lower() for x in open(PATH_WORDLISTS + '/First-person', 'r').read().splitlines()]
SECOND_PERSON_PRONOUNS = [x.lower() for x in open(PATH_WORDLISTS + '/Second-person', 'r').read().splitlines()]
THIRD_PERSON_PRON = [x.lower() for x in open(PATH_WORDLISTS + '/Third-person', 'r').read().splitlines()]
COORD_CONJUNCTIONS = ['CC']
COLONS_SEMI_COLONS = [';', ':']
PARENTHESES = ['(', ')']
COMMON_NOUNS = ['NN', 'NNS']
ADVERBS = ['RB', 'RBR', 'RBS']
PAST_TENSE_VERBS_TAG = ["VBN", "VBD"]
PROPER_NOUNS_TAG = ["NNP", "NNPS"]
WH_Words_TAG = ["WDT", "WP", "WP$", "WRB"]
FUTURE_TENSE = ['\'ll', 'will', 'gonna']

ATTR = "@attribute"

def isFrsPersonPron(tokenTag):
    token = getToken(tokenTag)

    return token.lower() in FIRST_PERSON_PRON

def isSecPersonPron(tokenTag):
    token = getToken(tokenTag)

    return token.lower() in SECOND_PERSON_PRONOUNS

def isThirdPersonPron(tokenTag):
    token = getToken(tokenTag)

    return token.lower() in THIRD_PERSON_PRON

def isCoordConj(tokenTag):
    tag = getTag(tokenTag)

    return tag.upper() in COORD_CONJUNCTIONS

def isPastTenseVerbs(tokenTag):
    tag = getTag(tokenTag)

    return tag.upper() in PAST_TENSE_VERBS_TAG

def isFutureTenseVerbs(tokenTag):
    token = getToken(tokenTag)

    return token.lower() in FUTURE_TENSE

def isCommas(tokenTag):
    token = getToken(tokenTag)

    return token == ","

def isColonsSemiColons(tokenTag):
    token = getToken(tokenTag)

    return token in COLONS_SEMI_COLONS

def isDashes(tokenTag):
    token = getToken(tokenTag)
    if re.match("^-+$", token):
        return True
    else:
        return False

def isParentheses(tokenTag):
    token = getToken(tokenTag)

    return token in PARENTHESES

def isEllipses(tokenTag):
    token = getToken(tokenTag)
    if re.match("^\.{3,}$", tokenTag):
        return True
    else:
        return False

def isCommonNouns(tokenTag):
    tag = getTag(tokenTag)

    return tag.upper() in COMMON_NOUNS

def isProperNouns(tokenTag):
    tag = getTag(tokenTag)

    return tag.upper() in PROPER_NOUNS_TAG

def isAdverbs(tokenTag):
    tag = getTag(tokenTag)

    return tag.upper() in ADVERBS

def iswhWords(tokenTag):
    tag = getTag(tokenTag)

    return tag.upper() in WH_Words_TAG

def isModernSlangAcroynms(tokenTag):
    token = getToken(tokenTag)

    return token.lower() in SLANGS

def isUpperCaseWord(tokenTag):
    token = getToken(tokenTag)

    return len(token) >= 2 and token.isupper()

def getToken(tokenTag):
    return tokenTag.split('/')[0]

def getTag(tokenTag):
    return tokenTag.split('/')[1]

def getSentenceLength(sentence):
    return len(list(re.finditer("\S+/\S+\s", sentence)))

def isWordToken(token):
    pattern = re.compile("^\w+$")

    return pattern.match(token) != None

def gatherFeatureInfo(fileName):
    twtFile = open(fileName, 'r')
    taggedTweets = twtFile.read()
    tweets = re.finditer("<A=(\d)>\n((?:\S+/\S+\s+)+)", taggedTweets)
    res = []
    tokenIdentifiers = [isFrsPersonPron, isSecPersonPron, isThirdPersonPron, isCoordConj, isPastTenseVerbs, isFutureTenseVerbs, isCommas, isColonsSemiColons, isDashes, isParentheses, isEllipses, isCommonNouns, isProperNouns, isAdverbs, iswhWords, isModernSlangAcroynms, isUpperCaseWord]
    for tweet in tweets:
        twtInfo = [0] * 21
        twtInfo[-1] = int(tweet.group(1))
        sentences = filter(None, tweet.group(2).split('\n'))
        numOfSentence = len(sentences)
        twtInfo[-2] = numOfSentence
        numOfWordTokens = 0
        for sentence in sentences:
            twtInfo[-4] = twtInfo[-4] + getSentenceLength(sentence)
            tokenTags = re.finditer("(\S+/\S+)", sentence)
            for tokenTag in tokenTags:
                tokenTagText = tokenTag.group()
                token = getToken(tokenTagText)
                if (isWordToken(token)):
                    numOfWordTokens += 1
                    twtInfo[-3] = twtInfo[-3] + len(token)
                for i in range(len(tokenIdentifiers)):
                    twtInfo[i] = twtInfo[i] + tokenIdentifiers[i](tokenTagText)
        twtInfo[-4] = twtInfo[-4] / numOfSentence
        twtInfo[-3] = twtInfo[-3] / numOfWordTokens
        res.append(twtInfo)
    return res

if __name__ == "__main__":
    inputFile = ''
    outputFile = ''
    maxNumOfTweetsPerClass = None
    if len(sys.argv) == 3:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]
    elif len(sys.argv) == 4:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]
        maxNumOfTweetsPerClass = int(sys.argv[3])
    else:
        print 'usage: buildarff.py <inputFile> <outputFile> [<maxNumOfTweetsPerClass>]'
        sys.exit()

    esFile = open(outputFile, "w")
    esFile.write("@relation TweetsFeatureInformation\n\n")
    esFile.write(ATTR + " FirstPersonPronouns numeric\n")
    esFile.write(ATTR + " SecondPersonPronouns numeric\n")
    esFile.write(ATTR + " ThirdPersonPronouns numeric\n")
    esFile.write(ATTR + " CoordinatingConjunctions numeric\n")
    esFile.write(ATTR + " Past-tenseVerbs numeric\n")
    esFile.write(ATTR + " Future-tenseVerbs numeric\n")
    esFile.write(ATTR + " Commas numeric\n")
    esFile.write(ATTR + " ColonsAndSemi-colons numeric\n")
    esFile.write(ATTR + " Dashes numeric\n")
    esFile.write(ATTR + " Parentheses numeric\n")
    esFile.write(ATTR + " Ellipses numeric\n")
    esFile.write(ATTR + " CommonNouns numeric\n")
    esFile.write(ATTR + " ProperNouns numeric\n")
    esFile.write(ATTR + " Adverbs numeric\n")
    esFile.write(ATTR + " wh-words numeric\n")
    esFile.write(ATTR + " ModernSlangAcroynms numeric\n")
    esFile.write(ATTR + " WordsAllInUpperCase numeric\n")
    esFile.write(ATTR + " AvgLengthOfSentences numeric\n")
    esFile.write(ATTR + " AvgLengthOfTokens numeric\n")
    esFile.write(ATTR + " NumOfSentences numeric\n")
    esFile.write(ATTR + " Class {0, 4}\n\n")
    esFile.write("@data\n")
    infoList = gatherFeatureInfo(inputFile)
    for info in infoList:
        esFile.write(','.join(str(x) for x in info) + "\n")


