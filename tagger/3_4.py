import os
import re
from scipy import stats

def splitTrainingInstances(fileName, classifier):
    inputFile = open(fileName, 'r')
    trainingInstances = inputFile.read()
    tweets = re.finditer("<A=(\d)>\n((?:\S+/\S+\s+)+)", trainingInstances)
    accuracies = []
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
    outputFile = open("3.4output_" + classifier +  ".txt", "w", 0) 
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
        os.system("java -cp /u/cs401/WEKA/weka.jar " + classifier + " -t trainingFile.arff -T testFile.arff > temp.txt")
        tempOutput = open("temp.txt", "r")
        result = ''.join(tempOutput.readlines()[-19:])
        outputFile.write(result)
        accurInfo = re.finditer("Correctly Classified Instances\s+\d+\s+(\d+.?\d+\s+%)", result)
        accuracy = accurInfo.next().group(1)
        outputFile.write("Accuracy: " + accuracy + "\n")
        accuracies.append(float(accuracy.split(' ')[0]))
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
    outputFile.close()
    return accuracies

if __name__ == "__main__":
    os.system("python twtt.py /u/cs401/A1/tweets/training.1600000.processed.noemoticon.csv 141 train.twt")
    classifiers = ['weka.classifiers.trees.J48', 'weka.classifiers.bayes.NaiveBayes', 'weka.classifiers.functions.SMO']
    accuracy_dict = {}
    for classifier in classifiers:
        accuracy_dict[classifier] = splitTrainingInstances("train.twt", classifier)

    outputFile = open("3.4output_pvalue.txt", "w", 0)
    outputFile.write('weka.classifiers.trees.J48 and weka.classifiers.bayes.NaiveBayes\n')
    outputFile.write(str(stats.ttest_rel(accuracy_dict['weka.classifiers.trees.J48'], accuracy_dict['weka.classifiers.bayes.NaiveBayes'])) + '\n\n')

    outputFile.write('weka.classifiers.bayes.NaiveBayes and weka.classifiers.functions.SMO\n')
    outputFile.write(str(stats.ttest_rel(accuracy_dict['weka.classifiers.bayes.NaiveBayes'], accuracy_dict['weka.classifiers.functions.SMO'])) + '\n\n')

    outputFile.write('weka.classifiers.functions.SMO and weka.classifiers.trees.J48\n')
    outputFile.write(str(stats.ttest_rel(accuracy_dict['weka.classifiers.functions.SMO'], accuracy_dict['weka.classifiers.trees.J48'])) + '\n\n')

    outputFile.close()


