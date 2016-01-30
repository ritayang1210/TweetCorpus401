PATH_WORDLISTS = './Wordlists'

SECOND_PERSON_PRONOUNS = ['you', 'your', 'yours', 'u', 'ur', 'urs']
COORD_CONJUNCTIONS = ['for', 'and', 'nor', 'but', 'or', 'yet', 'so' , 'yet', 'and', 'for', 'nor', 'or', 'but', 'so', 'for', 'or', 'nor', 'yet', 'but', 'and', 'so']
FUTURE_TENSE = ['\'ll', 'will', 'gonna']
COLONS_SEMI_COLONS = [';', ':']
PARENTHESES = ['(', ')']
COMMON_NOUNS = ['NN', 'NNS']
ADVERBS = ['RB', 'RBR', 'RBS']

def isFrsPersonPron(token):
    return False

def isSecPersonPron(tokenTage):
    token = getToken(tokenLabel)

    return token.lower() in SECOND_PERSON_PRONOUNS

def isThirdPersonPron(token):
    return False

def isCoordConj(tokenLabel):
    token = getToken(tokenLabel)

    return token.lower() in COORD_CONJUNCTIONS

def isPastTenseVerbs(token):
    return False

def isFutureTenseVerbs(tokenLabel):
    token = getToken(tokenLabel)

    return token.lower() in FUTURE_TENSE

def isCommas(token):
    return False

def isColonsSemi_colons(tokenLabel):
    token = getToken(tokenLabel)

    return token in COLONS_SEMI_COLONS

def isDashes(token):
    return False

def isParentheses(tokenLabel):
    token = getToken(tokenLabel)

    return token in PARENTHESES

def isEllipses(token):
    return False

def isCommonNouns(tokenLabel):
    tag = getLabel(tokenLabel)

    return tag.upper() in COMMON_NOUNS

def isProperNouns(tokenLabel):
    return False

def isAdverbs(token):
    tag = getLabel(tokenLabel)

    return tag.upper() in ADVERBS

def iswhWords(token):
    return False

def isModernSlangAcroynms(token):
    file = open(file_name, 'r')
    lines = file.readlines()

def isUpperCaseWord(token):
    return False

def getToken(tokenLabel):
    return tokenLabel.split('/')[0]

def getLabel(tokenLabel):
    return tokenLabel.split('/')[1]

# def avgLenOfSentences(tweet):
#     return

