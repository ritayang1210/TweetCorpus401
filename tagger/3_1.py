import os

if __name__ == '__main__':
    # Generate .twt files
    os.system('python twtt.py  /u/cs401/A1/tweets/testdata.manualSUBSET.2009.06.14.csv test.twt')
    os.system('python twtt.py  /u/cs401/A1/tweets/training.1600000.processed.noemoticon.csv 141 train.twt')

    # Generate .arff files
    os.system('python buildarff.py test.twt test.arff')
    os.system('python buildarff.py train.twt train.arff 5500')

    os.system('java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t train.arff -T test.arff > 3.1output_SVM.txt')
    os.system('java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t train.arff -T test.arff > 3.1output_NaiveBayes.txt')
    os.system('java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 -t train.arff -T test.arff > 3.1output_DecisionTrees.txt')

