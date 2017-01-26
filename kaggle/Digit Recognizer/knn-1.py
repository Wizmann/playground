#coding=utf-8
import sys
import csv
import numpy as np
import multiprocessing
import functools
import psutil
import heapq
from scipy.spatial import distance

THRESHOLD = 1

def vector_classify(vector):
    res = np.array(map(lambda x: 1 if x else 0, vector))
    return res

def predict(train_data, cur_vector):
    result, mini = -1, 10 ** 10
    for (label, vector) in train_data:
        diff = distance.euclidean(vector, cur_vector)
        if diff < mini:
            mini = diff
            result = label
    return result 

def test():
    train_data = [
            (0, [0, 0, 0]),
            (1, [1, 1, 1]),
    ]
    cur_vector = [0, 1, 0]
    assert predict(train_data, cur_vector) == 0

if __name__ == '__main__':
    test()
    train_data = []
    with open(sys.argv[1]) as data_file:
        reader = csv.reader(data_file, delimiter=',')
        for i, row in enumerate(reader):
            if not i:
                continue
            digit, vector = int(row[0]), vector_classify(map(int, row[1:]))
            train_data.append((digit, vector))

    print 'ImageId,Label'
    with open(sys.argv[2]) as test_file:
        reader = csv.reader(test_file, delimiter=',')
        tests = []
        for i, row in enumerate(reader):
            if not i:
                continue
            for i in xrange(28):
                for j in xrange(28):
                    sys.stdout.write('%d' % (1 if int(row[i * 28 + j]) else 0))
                sys.stdout.write('\n')
            print '==='
            vector = vector_classify(map(int, row))
            tests.append(vector)

        pool = multiprocessing.Pool(processes=8)
        results = pool.map(functools.partial(predict, train_data), tests, chunksize=100)
        for i, result in enumerate(results):
            print "%d,%d" % (i + 1 ,result)
        pool.close()
        pool.join()

