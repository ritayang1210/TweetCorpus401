import re
import sys

PATH_WORDLISTS = '/u/cs401/Wordlists'
CLASSES_TO_COMPUTE = [0, 4]

FIRST_PERSON_PRON = [x.lower() for x in open(PATH_WORDLISTS + '/First-person', 'r').read().splitlines()]
SECOND_PERSON_PRONOUNS = [x.lower() for x in open(PATH_WORDLISTS + '/Second-person', 'r').read().splitlines()]
THIRD_PERSON_PRON = [x.lower() for x in open(PATH_WORDLISTS + '/Third-person', 'r').read().splitlines()]
COORD_CONJUNCTIONS = [x.lower() for x in open(PATH_WORDLISTS + '/Conjunct', 'r').read().splitlines()]
PAST_TENSE_VERBS_TAG = ["VBN", "VBD"]
FUTURE_TENSE = ['\'ll', 'will', 'gonna']
COLONS_SEMI_COLONS = [';', ':']
PARENTHESES = ['(', ')']
COMMON_NOUNS = ['NN', 'NNS']
PROPER_NOUNS_TAG = ["NNP", "NNPS"]
ADVERBS = ['RB', 'RBR', 'RBS']
WH_WORDS_TAG = ["WDT", "WP", "WP$", "WRB"]
SLANGS = [x.lower() for x in open(PATH_WORDLISTS + '/Slang', 'r').read().splitlines()]

ATTR = "@attribute"

def isFrsPersonPron(tokenTag):
    '''
    First person Pron identifier.
    '''
    token = getToken(tokenTag)

    return token.lower() in FIRST_PERSON_PRON

def isSecPersonPron(tokenTag):
    '''
    Second person Pron identifier.
    '''
    token = getToken(tokenTag)

    return token.lower() in SECOND_PERSON_PRONOUNS

def isThirdPersonPron(tokenTag):
    '''
    Third person Pron identifier.
    '''
    token = getToken(tokenTag)

    return token.lower() in THIRD_PERSON_PRON

def isCoordConj(tokenTag):
    '''
    Coordinating conjunctions identifier.
    '''
    token = getToken(tokenTag)

    return token.lower() in COORD_CONJUNCTIONS or getTag(tokenTag).upper() == 'CC'

def isPastTenseVerbs(tokenTag):
    '''
    Past-tense verbs identifier.
    '''
    tag = getTag(tokenTag)

    return tag.upper() in PAST_TENSE_VERBS_TAG

def isFutureTenseVerbs(tokenTag):
    '''
    Future-tense verbs identifier.
    '''
    token = getToken(tokenTag)

    return token.lower() in FUTURE_TENSE

def isCommas(tokenTag):
    '''
    Commas identifier.
    '''
    token = getToken(tokenTag)

    return token == ","

def isColonsSemiColons(tokenTag):
    '''
    Colons and semi-colons identifier.
    '''
    token = getToken(tokenTag)

    return token in COLONS_SEMI_COLONS

def isDashes(tokenTag):
    '''
    Dashes identifier.
    '''
    token = getToken(tokenTag)

    return re.match("-+", token) != None

def isParentheses(tokenTag):
    '''
    Parentheses identifier.
    '''
    token = getToken(tokenTag)

    return token in PARENTHESES

def isEllipses(tokenTag):
    '''
    Ellipses identifier.
    '''
    token = getToken(tokenTag)

    return re.match("\.{3,}", tokenTag) != None

def isCommonNouns(tokenTag):
    '''
    Common nouns identifier.
    '''
    tag = getTag(tokenTag)

    return tag.upper() in COMMON_NOUNS

def isProperNouns(tokenTag):
    '''
    Proper nouns identifier.
    '''
    tag = getTag(tokenTag)

    return tag.upper() in PROPER_NOUNS_TAG

def isAdverbs(tokenTag):
    '''
    Adverbs identifier.
    '''
    tag = getTag(tokenTag)

    return tag.upper() in ADVERBS

def isWhWords(tokenTag):
    '''
    wh-words identifier.
    '''
    tag = getTag(tokenTag)

    return tag.upper() in WH_WORDS_TAG

def isModernSlangAcroynms(tokenTag):
    '''
    Modern slang acroynms identifier.
    '''
    token = getToken(tokenTag)

    return token.lower() in SLANGS

def isUpperCaseWord(tokenTag):
    '''
    Words all in upper case identifier.
    '''
    token = getToken(tokenTag)

    return len(token) >= 2 and token.isupper()

def getToken(tokenTag):
    '''
    Get the token from given token/tag pair.
    '''
    return tokenTag.split('/')[0]

def getTag(tokenTag):
    '''
    Get the tag from given token/tag pair.
    '''
    return tokenTag.split('/')[1]

def getSentenceLength(sentence):
    '''
    Get length of given sentence.
    '''
    return len(list(re.finditer("\S+/\S+\s", sentence)))

def isWordToken(token):
    '''
    Identify if given token is a word.
    '''
    pattern = re.compile("^\w+$")

    return pattern.match(token) != None

def gatherFeatureInfo(fileName, maxNumOfTweetsPerClass):
    '''
    Gather the feature information from a given file. Each class will not contain more feature lines than the maxNumOfTweetsPerClass provided.
    '''
    twtFile = open(fileName, 'r')
    numPerClass = {}
    for classToCompute in CLASSES_TO_COMPUTE:
        # Init the counter for each class
        numPerClass[classToCompute] = 0
    taggedTweets = twtFile.read()
    # regex used to fetch the next tweet
    tweets = re.finditer("<A=(\d)>\n((?:\S+/\S+\s+)+)", taggedTweets)
    res = []
    # Init the list of identifiers
    tokenIdentifiers = [isFrsPersonPron, isSecPersonPron, isThirdPersonPron, isCoordConj, isPastTenseVerbs, isFutureTenseVerbs, isCommas, isColonsSemiColons, isDashes, isParentheses, isEllipses, isCommonNouns, isProperNouns, isAdverbs, isWhWords, isModernSlangAcroynms, isUpperCaseWord]
    for tweet in tweets:
        # Process each tweet
        twtInfo = [0] * 21
        tweetClass = int(tweet.group(1))
        twtInfo[-1] = tweetClass
        if not tweetClass in numPerClass or numPerClass[tweetClass] >= maxNumOfTweetsPerClass:
            # Skip if already exceed the maxNumOfTweetsPerClass for this class
            continue
        numPerClass[tweetClass] = numPerClass[tweetClass] + 1

        # Split tweet into sentences
        sentences = filter(None, tweet.group(2).split('\n'))
        numOfSentence = len(sentences)
        twtInfo[-2] = numOfSentence
        numOfWordTokens = 0
        for sentence in sentences:
            # Calculate sentence length
            twtInfo[-4] = twtInfo[-4] + getSentenceLength(sentence)
            tokenTags = re.finditer("(\S+/\S+)", sentence)
            for tokenTag in tokenTags:
                tokenTagText = tokenTag.group()
                token = getToken(tokenTagText)
                if (isWordToken(token)):
                    # Count length of each word token
                    numOfWordTokens += 1
                    twtInfo[-3] = twtInfo[-3] + len(token)
                for i in range(len(tokenIdentifiers)):
                    # Run each identifier for each token
                    twtInfo[i] = twtInfo[i] + tokenIdentifiers[i](tokenTagText)
        # Calculate averages
        twtInfo[-4] = float(twtInfo[-4]) / numOfSentence
        twtInfo[-3] = float(twtInfo[-3]) / numOfWordTokens
        res.append(twtInfo)
    return res

if __name__ == "__main__":
    inputFile = ''
    outputFile = ''
    maxNumOfTweetsPerClass = sys.maxint

    # Read command line inputs first
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

    # Build the .arff file
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
    infoList = gatherFeatureInfo(inputFile, maxNumOfTweetsPerClass)
    for info in infoList:
        esFile.write(','.join(str(x) for x in info) + "\n")


