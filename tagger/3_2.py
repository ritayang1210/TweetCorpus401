import os

if __name__ == '__main__':
    # Generate .twt files
    os.system('python twtt.py ../tweets/testdata.manual.2009.06.14.csv test.twt')
    os.system('python twtt.py ../tweets/training.1600000.processed.noemoticon.csv 141 train.twt')

    os.system('python buildarff.py test.twt test.arff')
    n = 250
    while n <= 2750:
        # Generate .arff files
        os.system('python buildarff.py train.twt train.arff ' + str(n))
        os.system('java -cp ../WEKA/weka.jar weka.classifiers.trees.J48 -t train.arff -T test.arff > ' + str(n * 2) + '-result.txt')
        print('Finished with data size ' + str(n * 2) + '...')
        n += 250
