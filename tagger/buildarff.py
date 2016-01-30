import re

PATH_WORDLISTS = '../Wordlists'

SECOND_PERSON_PRONOUNS = open(PATH_WORDLISTS + '/Second-person', 'r').read().splitlines()
SLANGS = open(PATH_WORDLISTS + '/Slang', 'r').read().splitlines()
COORD_CONJUNCTIONS = ['CC']
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
    if len(token) >= 2 and token.isupper():
        return True
    else:
        return False

def getToken(tokenTag):
    return tokenTag.split('/')[0]

def getTag(tokenTag):
    return tokenTag.split('/')[1]

# def avgLenOfSentences(tweet):
#     return

print isSecPersonPron('youRsx/NN')