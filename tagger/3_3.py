import os

if __name__ == '__main__':
    # Generate .twt files
    os.system('python twtt.py /u/cs401/A1/tweets/training.1600000.processed.noemoticon.csv 141 train.twt')

    os.system('python buildarff.py train.twt train.arff 500')
    os.system('echo \'================ Result for training data with size 500 ================\' > 3.3output.txt')
    os.system('sh /u/cs401/WEKA/infogain.sh train.arff >> 3.3output.txt')

    os.system('python buildarff.py train.twt train.arff 5500')
    os.system('echo \'================ Result for training data with size 5500 ================\' >> 3.3output.txt')
    os.system('sh /u/cs401/WEKA/infogain.sh train.arff >> 3.3output.txt')