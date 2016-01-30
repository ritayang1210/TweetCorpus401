FIRST_PERSON_PRON = [i, me, my, mine, we, us, our, ours]
THIRD_PERSON_PRON = [he, him, his, she, her, hers, it, its, they, them, their, theirs]
PAST_TENSE_VERBS_TAG = [VBN, VBD]
PROPER_NOUNS_TAG = [NNP, NNPS]
WH_Words_TAG = [WDT, WP, WP$, WRB]

def isFrsPersonPron(tokenTag):
    token = getToken(tokenTag)
    return token.lower() in FIRST_PERSON_PRON

def isSecPersonPron(token):
    return False

def isThirdPersonPron(tokenTag):
    token = getToken(tokenTag)
    return token.lower() in THIRD_PERSON_PRON

def isCoordConj(token):
    return False

def isPastTenseVerbs(tokenTag):
    tag = getLabel(tokenTag)
    return tag.upper() in PAST_TENSE_VERBS_TAG

def isFutureTenseVerbs(token):
    return False

def isCommas(tokenTag):
    token = getToken(tokenTag)
    return token == ","

def isColonsSemi_colons(token):
    return False

def isDashes(tokenTag):
    token = getToken(tokenTag)
    if re.match("^-+$", token):
        return True
    else:
        return False

def isParentheses(token):
    return False

def isEllipses(tokenTag):
    token = getToken(tokenTag)
    if re.match("^\.{3,}$", tokenTag):
        return True
    else:
        return False

def isCommonNouns(token):
    return False

def isProperNouns(tokenTag):
    tag = getLabel(tokenTag)
    return tag.upper() in PROPER_NOUNS_TAG

def isAdverbs(token):
    return False

def iswhWords(tokenTag):
    tag = getLabel(tokenTag)
    return tag.upper() in WH_Words_TAG

def isModernSlangAcroynms(token):
    return False

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

