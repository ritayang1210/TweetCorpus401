import re

PATH_WORDLISTS = './Wordlists'

SECOND_PERSON_PRONOUNS = ['you', 'your', 'yours', 'u', 'ur', 'urs']
COORD_CONJUNCTIONS = ['for', 'and', 'nor', 'but', 'or', 'yet', 'so' , 'yet', 'and', 'for', 'nor', 'or', 'but', 'so', 'for', 'or', 'nor', 'yet', 'but', 'and', 'so']
FUTURE_TENSE = ['\'ll', 'will', 'gonna']
COLONS_SEMI_COLONS = [';', ':']
PARENTHESES = ['(', ')']
COMMON_NOUNS = ['NN', 'NNS']
ADVERBS = ['RB', 'RBR', 'RBS']
FIRST_PERSON_PRON = ["i", "me", "my", "mine", "we", "us", "our", "ours"]
THIRD_PERSON_PRON = ["he", "him", "his", "she", "her", "hers", "it", "its", "they", "them", "their", "theirs"]
PAST_TENSE_VERBS_TAG = ["VBN", "VBD"]
PROPER_NOUNS_TAG = ["NNP", "NNPS"]
WH_Words_TAG = ["WDT", "WP", "WP$", "WRB"]

def isFrsPersonPron(tokenTag):
    token = getToken(tokenTag)

    return token.lower() in FIRST_PERSON_PRON

def isSecPersonPron(tokenTage):
    token = getToken(tokenLabel)

    return token.lower() in SECOND_PERSON_PRONOUNS

def isThirdPersonPron(tokenTag):
    token = getToken(tokenTag)
    return token.lower() in THIRD_PERSON_PRON

def isCoordConj(tokenLabel):
    token = getToken(tokenLabel)

    return token.lower() in COORD_CONJUNCTIONS

def isPastTenseVerbs(tokenTag):
    tag = getLabel(tokenTag)
    return tag.upper() in PAST_TENSE_VERBS_TAG

def isFutureTenseVerbs(tokenLabel):
    token = getToken(tokenLabel)

    return token.lower() in FUTURE_TENSE

def isCommas(tokenTag):
    token = getToken(tokenTag)
    return token == ","

def isColonsSemi_colons(tokenLabel):
    token = getToken(tokenLabel)

    return token in COLONS_SEMI_COLONS

def isDashes(tokenTag):
    token = getToken(tokenTag)
    if re.match("^-+$", token):
        return True
    else:
        return False

def isParentheses(tokenLabel):
    token = getToken(tokenLabel)

    return token in PARENTHESES

def isEllipses(tokenTag):
    token = getToken(tokenTag)
    if re.match("^\.{3,}$", tokenTag):
        return True
    else:
        return False

def isCommonNouns(tokenLabel):
    tag = getLabel(tokenLabel)

    return tag.upper() in COMMON_NOUNS

def isProperNouns(tokenTag):
    tag = getLabel(tokenTag)
    
    return tag.upper() in PROPER_NOUNS_TAG

def isAdverbs(token):
    tag = getLabel(tokenLabel)

    return tag.upper() in ADVERBS

def iswhWords(tokenTag):
    tag = getLabel(tokenTag)
    return tag.upper() in WH_Words_TAG

def isModernSlangAcroynms(token):
    file = open(file_name, 'r')
    lines = file.readlines()

def isUpperCaseWord(tokenTag):
    token = getToken(tokenTag)
    if len(token) >= 2 and token.isupper():
        return True
    else:
        return False

def getToken(tokenLabel):
    return tokenLabel.split('/')[0]

def getLabel(tokenLabel):
    return tokenLabel.split('/')[1]

# def avgLenOfSentences(tweet):
#     return

