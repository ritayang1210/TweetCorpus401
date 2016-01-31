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
    for i in range(len(groups)):
        testFile = open("testFile.twt", "w", 0) 
        testFile.write(''.join(groups[i]))
        testFile.flush()
        testFile.close()
        os.system("python buildarff.py testFile.twt testFile.arff")

        trainingFile = open("trainingFile.twt", "w", 0)
        for j in range(len(groups)):
            if j != i: 
                trainingFile.write(''.join(groups[j]))
        trainingFile.flush()
        trainingFile.close()
        os.system("python buildarff.py trainingFile.twt trainingFile.arff")
        os.system("java -cp ../WEKA/weka.jar weka.classifiers.trees.J48 -t trainingFile.arff -T testFile.arff > 3_4output.txt")

if __name__ == "__main__":
    # os.system("python twtt.py ../tweets/training.1600000.processed.noemoticon.csv 141 train.twt")
    splitTrainingInstances("train.twt")

