import json
import math
import os

import openpyxl
import pandas as pd
import numpy as np
from xlutils.copy import copy
import xlwt
import xlrd

#获取每个蛋白的功能注释
def readUniprot(parent_path):
    file = "data/crossValidation/firstExperiments/train.txt"
    testfile = "data/crossValidation/firstExperiments/test.txt"
    dataset = list(np.loadtxt(file, dtype=np.str))
    candidate = np.loadtxt(testfile, dtype=np.str)

    for i in range(len(candidate)):
        if candidate[i] in dataset:
            dataset.remove(candidate[i])
    test_path = os.path.join(parent_path, r'data\crossValidation\firstExperiments\train2.txt')
    np.savetxt(test_path, dataset, fmt='%s')

if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    readUniprot(ROOT_DIR)