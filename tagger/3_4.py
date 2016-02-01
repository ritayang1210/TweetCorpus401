import os
import re

def splitTrainingInstances(fileName):
    inputFile = open(fileName, 'r')
    trainingInstances = inputFile.read()
    tweets = re.finditer("<A=(\d)>\n((?:\S+/\S+\s+)+)", trainingInstances)
    groups = [[], [], [], [], [], [], [], [], [], []]
    i = 0
    while i < 10:
        k = 0
        while k < 550:
            groups[i].append(tweets.next().group())
            k += 1
        i += 1

    i = 0
    while i < 10:
        k = 0
        while k < 550:
            groups[i].append(tweets.next().group())
            k += 1
        i += 1
    outputFile = open("3_4output.txt", "w", 0) 
    for i in range(len(groups)):
        testFile = open("testFile.twt", "w", 0) 
        testFile.write(''.join(groups[i]))
        testFile.flush()
        testFile.close()
        os.system("python buildarff.py testFile.twt testFile.arff")

        trainingFile = open("trainingFile.twt", "w", 0)
        outputFile.write('================ Result for partition d' + str(i+1) + ' as test set ================')
        for j in range(len(groups)):
            if j != i: 
                trainingFile.write(''.join(groups[j]))
        trainingFile.flush()
        trainingFile.close()

        os.system("python buildarff.py trainingFile.twt trainingFile.arff")
        os.system("java -cp ../WEKA/weka.jar weka.classifiers.trees.J48 -t trainingFile.arff -T testFile.arff > temp.txt")
        tempOutput = open("temp.txt", "r")
        result = ''.join(tempOutput.readlines()[-19:])
        outputFile.write(result)
        accurInfo = re.finditer("Correctly Classified Instances\s+\d+\s+(\d+.?\d+\s+%)", result)
        outputFile.write("Accuracy: " + accurInfo.next().group(1) + "\n")
        precInfo = re.finditer("(\d+)\s+(\d+)\s+\|\s+a\s+=\s+\d+\s+(\d+)\s+(\d+)", result)
        val = precInfo.next()
        precA = float(val.group(1))/(float(val.group(1)) + float(val.group(3)))
        precB = float(val.group(4))/(float(val.group(2)) + float(val.group(4)))
        avgPrec = (precA + precB)/2
        recallA = float(val.group(1))/(float(val.group(1)) + float(val.group(2)))
        recallB = float(val.group(4))/(float(val.group(3)) + float(val.group(4)))
        avgRecall = (recallA + recallB)/2
        outputFile.write("Average precision: " + str(avgPrec)+ "\n")
        outputFile.write("Average recall: " + str(avgRecall) + "\n\n")

    outputFile.write("================ Average Result Report ================")
    outputFile.write("")

if __name__ == "__main__":
    # os.system("python twtt.py ../tweets/training.1600000.processed.noemoticon.csv 141 train.twt")
    splitTrainingInstances("train.twt")

