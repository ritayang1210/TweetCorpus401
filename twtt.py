#import NLPlib

def read_file(file_name):
    """(str of file name) ->Table
    Input a string which is the file name of a table
    """
    file = open(file_name, 'r')
    # read table to get all of the content of the table
    file_list = file.readlines()
    file.close()
    return file_list

def removeHTMLTagAttr(tweetText):
    #TODO
    return

def replaceHTMLChars(tweetText):
    #TODO
    return

def removeURL(tweetText):
    #TODO
    return

def removeFstCharOfUserNameHashTag(tweetText):
    #TODO
    return

def findLineEnding(tweetText):
    #TODO
    return

def separateBySpace(tweetText):
    #TODO
    return

def addTagToToken(tweetText):
    #TODO
    return

def addDemarcation(tweetText):
    #TODO
    return

if __name__ == "__main__":
    print (read_table("tweets/testdata.manual.2009.06.14.csv"))