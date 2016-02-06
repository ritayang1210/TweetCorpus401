# ibmTest.py
# 
# This file tests all 11 classifiers using the NLClassifier IBM Service
# previously created using ibmTrain.py
# 
# TODO: You must fill out all of the functions in this file following 
#       the specifications exactly. DO NOT modify the headers of any
#       functions. Doing so will cause your program to fail the autotester.
#
#       You may use whatever libraries you like (as long as they are available
#       on CDF). You may find json, request, or pycurl helpful.
#       You may also find it helpful to reuse some of your functions from ibmTrain.py.
#
import json
import sys
import requests
from urllib import quote
from ibmTrain import *

RESPONSE_DICT = None

def getClassifier(username,password):
    global RESPONSE_DICT
    if not RESPONSE_DICT:
        print 'calculate RESPONSE_DICT'
        url = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers"
        r = requests.get(url, auth=(username, password), headers={'Content-Type': 'application/json'})
        RESPONSE_DICT = json.loads(r.text)
        if "error" in RESPONSE_DICT:
            errorMsg = RESPONSE_DICT['error'] + ": " + RESPONSE_DICT['description']
            RESPONSE_DICT = None
            raise Exception(errorMsg)
    return RESPONSE_DICT.copy()

def get_classifier_ids(username,password):
    # Retrieves a list of classifier ids from a NLClassifier service 
    # an outputfile named ibmTrain#.csv (where # is n_lines_to_extract).
    #
    # Inputs: 
    #   username - username for the NLClassifier to be used, as a string
    #
    #   password - password for the NLClassifier to be used, as a string
    #
    #       
    # Returns:
    #   a list of classifier ids as strings
    #
    # Error Handling:
    #   This function should throw an exception if the classifiers call fails for any reason
    #
    
    #TODO: Fill in this function

    # url = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers"
    # parameters = ""
    # data = urllib.urlencode(parameters)
    # req = urllib2.Request(url, data)
    # response = urllib2.urlopen(req)
    # json = response.read()
        idList = []
        response_dict = getClassifier(username,password)
        for classifier in response_dict["classifiers"]:
            idList.append(classifier["classifier_id"])
        print idList
        return idList
    

def assert_all_classifiers_are_available(username, password, classifier_id_list):
    # Asserts all classifiers in the classifier_id_list are 'Available' 
    #
    # Inputs: 
    #   username - username for the NLClassifier to be used, as a string
    #
    #   password - password for the NLClassifier to be used, as a string
    #
    #   classifier_id_list - a list of classifier ids as strings
    #       
    # Returns:
    #   None
    #
    # Error Handling:
    #   This function should throw an exception if the classifiers call fails for any reason AND 
    #   It should throw an error if any classifier is NOT 'Available'
    #
    
    #TODO: Fill in this function
    for id in classifier_id_list:
        url = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/" + id
        r = requests.get(url, auth=(username, password), headers={'Content-Type': 'application/json'})
        response_dict = json.loads(r.text)
        if "error" in response_dict:
            errorMsg = response_dict['error'] + ": " + response_dict['description']
            raise Exception(errorMsg)
        print response_dict["status"]
        assert(response_dict["status"] == "Available")

def classify_single_text(username,password,classifier_id,text):
    # Classifies a given text using a single classifier from an NLClassifier 
    # service
    #
    # Inputs: 
    #   username - username for the NLClassifier to be used, as a string
    #
    #   password - password for the NLClassifier to be used, as a string
    #
    #   classifier_id - a classifier id, as a string
    #       
    #   text - a string of text to be classified, not UTF-8 encoded
    #       ex. "Oh, look a tweet!"
    #
    # Returns:
    #   A "classification". Aka: 
    #   a dictionary containing the top_class and the confidences of all the possible classes 
    #   Format example:
    #       {'top_class': 'class_name',
    #        'classes': [
    #                     {'class_name': 'myclass', 'confidence': 0.999} ,
    #                     {'class_name': 'myclass2', 'confidence': 0.001}
    #                   ]
    #       }
    #
    # Error Handling:
    #   This function should throw an exception if the classify call fails for any reason 
    #
    
    #TODO: Fill in this function
    tweet = quote(text)
    url = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/" + classifier_id + "/classify?text=" + tweet
    r = requests.get(url, auth=(username, password), headers={'Content-Type': 'application/json'})
    response_dict = json.loads(r.text)
    if "error" in response_dict:
        errorMsg = response_dict['error'] + ": " + response_dict['description']
        raise Exception(errorMsg)
    else:
        return dict((k, response_dict[k]) for k in ('top_class', 'classes'))

def classify_all_texts(username,password,input_csv_name):
    # Classifies all texts in an input csv file using all classifiers for a given NLClassifier
    # service.
    #
    # Inputs:
    #       username - username for the NLClassifier to be used, as a string
    #
    #       password - password for the NLClassifier to be used, as a string
    #
    #       input_csv_name - full path and name of an input csv file in the
    #              6 column format of the input test/training files
    #
    # Returns:
    #       A dictionary of lists of "classifications".
    #       Each dictionary key is the name of a classifier.
    #       Each dictionary value is a list of "classifications" where a
    #       "classification" is in the same format as returned by
    #       classify_single_text.
    #       Each element in the main dictionary is:
    #       A list of dictionaries, one for each text, in order of lines in the
    #       input file. Each element is a dictionary containing the top_class
    #       and the confidences of all the possible classes (ie the same
    #       format as returned by classify_single_text)
    #       Format example:
    #              {'classifiername':
    #                      [
    #                              {'top_class': 'class_name',
    #                              'classes': [
    #                                        {'class_name': 'myclass', 'confidence': 0.999} ,
    #                                         {'class_name': 'myclass2', 'confidence': 0.001}
    #                                          ]
    #                              },
    #                              {'top_class': 'class_name',
    #                              ...
    #                              }
    #                      ]
    #              , 'classifiername2':
    #                      [
    #                     ...
    #                      ]
    #              ...
    #              }
    #
    # Error Handling:
    #       This function should throw an exception if the classify call fails for any reason
    #       or if the input csv file is of an improper format.
    #
    inputFile = open(input_csv_name, 'r')
    inputLines = inputFile.readlines()
    idList = get_classifier_ids(username,password)
    response_dict = getClassifier(username,password)
    nameList = []
    for classifier in response_dict["classifiers"]:
        nameList.append(classifier["name"])

    classifications = {}
    i = 0
    while i < len(nameList):
        classifierDict = []
        j = 0
        while j < len(inputLines):
            text = inputLines[j].split(',"')[5][0:-2]
            temp = classify_single_text(username,password,idList[i],text)
            classifierDict.append(temp)
            j += 1
        classifications[nameList[i]] = classifierDict
        i += 1
    return classifications

def compute_accuracy_of_single_classifier(classifier_dict, input_csv_file_name):
    # Given a list of "classifications" for a given classifier, compute the accuracy of this
    # classifier according to the input csv file
    #
    # Inputs:
    #   classifier_dict - A list of "classifications". Aka:
    #       A list of dictionaries, one for each text, in order of lines in the 
    #       input file. Each element is a dictionary containing the top_class
    #       and the confidences of all the possible classes (ie the same
    #       format as returned by classify_single_text)     
    #       Format example:
    #           [
    #               {'top_class': 'class_name',
    #                'classes': [
    #                           {'class_name': 'myclass', 'confidence': 0.999} ,
    #                           {'class_name': 'myclass2', 'confidence': 0.001}
    #                           ]
    #               },
    #               {'top_class': 'class_name',
    #               ...
    #               }
    #           ]
    #
    #   input_csv_name - full path and name of an input csv file in the  
    #       6 column format of the input test/training files
    #
    # Returns:
    #   The accuracy of the classifier, as a fraction between [0.0-1.0] (ie percentage/100). \
    #   See the handout for more info.
    #
    # Error Handling:
    #   This function should throw an error if there is an issue with the 
    #   inputs.
    #
    
    #TODO: fill in this function
    inputFile = open(input_csv_file_name, "r")
    inputLines = inputFile.readlines()
    count = 0
    total = len(inputLines)
    i = 0
    while i < total:
        if classifier_dict[i]['top_class'] == inputLines[i][1]:
            count += 1
        i += 1
    return float(count) / total

def compute_average_confidence_of_single_classifier(classifier_dict, input_csv_file_name):
    # Given a list of "classifications" for a given classifier, compute the average 
    # confidence of this classifier wrt the selected class, according to the input
    # csv file. 
    #
    # Inputs:
    #   classifier_dict - A list of "classifications". Aka:
    #       A list of dictionaries, one for each text, in order of lines in the 
    #       input file. Each element is a dictionary containing the top_class
    #       and the confidences of all the possible classes (ie the same
    #       format as returned by classify_single_text)     
    #       Format example:
    #           [
    #               {'top_class': 'class_name',
    #                'classes': [
    #                           {'class_name': 'myclass', 'confidence': 0.999} ,
    #                           {'class_name': 'myclass2', 'confidence': 0.001}
    #                           ]
    #               },
    #               {'top_class': 'class_name',
    #               ...
    #               }
    #           ]
    #
    #   input_csv_name - full path and name of an input csv file in the  
    #       6 column format of the input test/training files
    #
    # Returns:
    #   The average confidence of the classifier, as a number between [0.0-1.0]
    #   See the handout for more info.
    #
    # Error Handling:
    #   This function should throw an error if there is an issue with the 
    #   inputs.
    #
    
    #TODO: fill in this function
    inputFile = open(input_csv_file_name, "r")
    lines = [line for line in inputFile.readlines() if line.strip()]

    class0_correct = 0
    class0_incorrect = 0
    class0_total = 0
    class4_correct = 0
    class4_incorrect = 0
    class4_total = 0

    for i in range(len(lines)):
        line = lines[i]
        actuall_class = line[1]
        predicted_class = classifier_dict[i]['top_class']
        confidence = 0.0
        for cla in classifier_dict[i]['classes']:
            if cla['class_name'] == actuall_class:
                confidence = cla['confidence']
                break
        class0_total += actuall_class == '0'
        class4_total += actuall_class == '4'
        class0_correct += confidence if predicted_class == actuall_class == '0' else 0.0
        class4_correct += confidence if predicted_class == actuall_class == '4' else 0.0
        class0_incorrect += confidence if predicted_class != actuall_class == '0' else 0.0
        class4_incorrect += confidence if predicted_class != actuall_class == '4' else 0.0

    return (class0_correct + class0_incorrect) / class0_total, (class4_correct + class4_incorrect) / class4_total

if __name__ == "__main__":

    input_test_data = "tweets/testdata.manualSUBSET.2009.06.14.csv"
    username = "7d6041e2-25af-4c5d-904e-9ef15a381aaa"
    password = "HL5SUjigee6W"
    idList = get_classifier_ids(username,password)
    #STEP 1: Ensure all 11 classifiers are ready for testing
    assert_all_classifiers_are_available(username, password, idList)
    
    #STEP 2: Test the test data on all classifiers
    clists = classify_all_texts(username, password, input_test_data)
    #STEP 3: Compute the accuracy for each classifier
    outputFile = open("4output.txt", "w")
    for classifier in clists:
        accuracy = compute_accuracy_of_single_classifier(clists[classifier], input_test_data)
        outputFile.write('acurracy of ' + str(classifier) + ": " + str(accuracy) + '\n\n')
    #STEP 4: Compute the confidence of each class for each classifier
        avg_class0_conf, avg_class4_conf = compute_average_confidence_of_single_classifier(clists[classifier], input_test_data)
        outputFile.write('average confidence of class 0 using classfier ' + str(classifier) + ": " + str(avg_class0_conf) + '\n')
        outputFile.write('average confidence of class 4 using classfier ' + str(classifier) + ": " + str(avg_class4_conf) + '\n\n')



