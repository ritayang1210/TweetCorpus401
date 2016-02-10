# ibmTrain.py
# 
# This file produces 11 classifiers using the NLClassifier IBM Service
# 
# TODO: You must fill out all of the functions in this file following 
#       the specifications exactly. DO NOT modify the headers of any
#       functions. Doing so will cause your program to fail the autotester.
#
#       You may use whatever libraries you like (as long as they are available
#       on CDF). You may find json, request, or pycurl helpful.
#

###IMPORTS###################################
import requests, json, sys
import os

###HELPER FUNCTIONS##########################

def convert_training_csv_to_watson_csv_format(input_csv_name, group_id, output_csv_name): 
    # Converts an existing training csv file. The output file should
    # contain only the 11,000 lines of your group's specific training set.
    #
    # Inputs:
    #   input_csv - a string containing the name of the original csv file
    #       ex. "my_file.csv"
    #
    #   output_csv - a string containing the name of the output csv file
    #       ex. "my_output_file.csv"
    #
    # Returns:
    #   None
    input_csv = open(input_csv_name, "r")
    inputLines = input_csv.readlines()
    output_csv = open(output_csv_name, "w")
    trainingData = inputLines[group_id * 5500: (group_id + 1) * 5500] + inputLines[800000 + group_id * 5500: 800000 + (group_id + 1) * 5500]
    for i in range(len(trainingData)):
        temp = trainingData[i].split(',"')

        tempTweet = '"' + temp[-1][:-2].strip() + '"' + ',' + temp[0][1:-1] + '\n'
        resTemp = tempTweet.replace("\t", "\\t")
        output_csv.write(resTemp.decode('utf-8','ignore').encode("utf-8"))

def extract_subset_from_csv_file(input_csv_file, n_lines_to_extract, output_file_prefix='ibmTrain'):
    # Extracts n_lines_to_extract lines from a given csv file and writes them to 
    # an outputfile named ibmTrain#.csv (where # is n_lines_to_extract).
    #
    # Inputs: 
    #   input_csv - a string containing the name of the original csv file from which
    #       a subset of lines will be extracted
    #       ex. "my_file.csv"
    #   
    #   n_lines_to_extract - the number of lines to extract from the csv_file, as an integer
    #       ex. 500
    #
    #   output_file_prefix - a prefix for the output csv file. If unspecified, output files 
    #       are named 'ibmTrain#.csv', where # is the input parameter n_lines_to_extract.
    #       The csv must be in the "watson" 2-column format.
    #       
    # Returns:
    #   None
    input_csv = open(input_csv_file, "r")
    inputLines = input_csv.readlines()
    outputFileName = output_file_prefix + str(n_lines_to_extract) + ".csv"
    output_csv = open(outputFileName, "w")
    countClass0 = 0
    countClass4 = 0
    i = 0
    while (countClass0 + countClass4) < n_lines_to_extract * 2 and i < len(inputLines):
        if (inputLines[i][-2] == str(0) and countClass0 < n_lines_to_extract):
            output_csv.write(inputLines[i])
            countClass0 += 1
        elif (inputLines[i][-2] == str(4) and countClass4 < n_lines_to_extract):
            output_csv.write(inputLines[i])
            countClass4 += 1
        i += 1


def create_classifier(username, password, n, input_file_prefix='ibmTrain'):
    # Creates a classifier using the NLClassifier service specified with username and password.
    # Training_data for the classifier provided using an existing csv file named
    # ibmTrain#.csv, where # is the input parameter n.
    #
    # Inputs:
    #   username - username for the NLClassifier to be used, as a string
    #
    #   password - password for the NLClassifier to be used, as a string
    #
    #   n - identification number for the input_file, as an integer
    #       ex. 500
    #
    #   input_file_prefix - a prefix for the input csv file, as a string.
    #       If unspecified data will be collected from an existing csv file 
    #       named 'ibmTrain#.csv', where # is the input parameter n.
    #       The csv must be in the "watson" 2-column format.
    #
    # Returns:
    #   A dictionary containing the response code of the classifier call, will all the fields 
    #   specified at
    #   http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/natural-language-classifier/api/v1/?curl#create_classifier
    #   
    #
    # Error Handling:
    #   This function should throw an exception if the create classifier call fails for any reason
    #   or if the input csv file does not exist or cannot be read.
    #('report.xls', open('report.xls', 'rb')
    
    #TODO: Fill in this function
    input_file_name = input_file_prefix + str(n) + '.csv'
    nlclassifier_service_url = 'https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers'
    files = {
        'training_data': open(input_file_name, 'rb'),
        'training_metadata': "{\"language\":\"en\",\"name\":\"Classifier " + str(n) + "\"}"
    }
    r = requests.post(nlclassifier_service_url,
                      auth=(username, password),
                      # headers={'Content-Type': 'application/multi-part/form-data'},
                      files=files)

    response_dict = json.loads(r.text)
    # if not 'status' in response_dict or response_dict['status'] in ['Training', 'Available']:
    #     if 'status_description' in response_dict:
    #         raise Exception(response_dict['status_description'])
    #     else:
    #         raise Exception(response_dict['description'])
    print r.text
    if "error" in response_dict:
    	errorMsg = response_dict['error'] + ": " + response_dict['description']
    	raise Exception(errorMsg)
    else:
    	return r

if __name__ == "__main__":
    
    ### STEP 1: Convert csv file into two-field watson format
    input_csv_name = '/u/cs401/A1/tweets/training.1600000.processed.noemoticon.csv'
    
    #DO NOT CHANGE THE NAME OF THIS FILE
    output_csv_name = 'training_11000_watson_style.csv'
    
    convert_training_csv_to_watson_csv_format(input_csv_name, 141, output_csv_name)
    
    
    ### STEP 2: Save 11 subsets in the new format into ibmTrain#.csv files
    
    #TODO: extract all 11 subsets and write the 11 new ibmTrain#.csv files
    #
    # you should make use of the following function call:
    #
    training_set_sizes = [500, 2500, 5000]
    for n_lines_to_extract in training_set_sizes:
        extract_subset_from_csv_file(output_csv_name, n_lines_to_extract)
    
    ### STEP 3: Create the classifiers using Watson
    
    #TODO: Create all 11 classifiers using the csv files of the subsets produced in 
    # STEP 2
    # 
    #
    # you should make use of the following function call
    username = '7d6041e2-25af-4c5d-904e-9ef15a381aaa'
    password = 'HL5SUjigee6W'

    for n in training_set_sizes:
        create_classifier(username, password, n, input_file_prefix='ibmTrain')

