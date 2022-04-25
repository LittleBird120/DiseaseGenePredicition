import pandas as pd
import numpy as np
import json
import os
import math
import time
import networkx as nx
from collections import OrderedDict

def getCandidatePro(candidateId_file):
    node_degreename = path + '/dataset/result/candidateID.txt'
    with open(candidateId_file, 'r') as f2:
        candidate = f2.readlines()

    with open(node_degreename, "w") as fw:
        for i in range(len(candidate)):
            every_candidateID = candidate[i].split("\t")[1]
            fw.write(every_candidateID)
            fw.write("\n")

if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    candidateId_file = path + "/dataset/result/geneIdConvert.txt"  #候选宿主蛋白
    candidateId = getCandidatePro(candidateId_file)