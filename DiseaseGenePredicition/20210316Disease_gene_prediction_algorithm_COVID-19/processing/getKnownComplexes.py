import os
import json
import pandas as pd
import numpy as np
import networkx as nx

def readknownComplex(parent_path):
    knownpro_file = os.path.join(parent_path, r'dataset\temp\humanComplex.json')
    with open(knownpro_file, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
    return json_data

def readknownpro(parent_path, complex_json_data):
    trainfile = os.path.join(parent_path, r'dataset\uploads\secondExperiments\train.txt')
    train_dataset = list(np.loadtxt(trainfile, dtype=np.str))

    complexList = []
    for i in range(len(complex_json_data)):
        knownComplex = complex_json_data[i]["subunits(UniProt IDs)"].split(";")
        share = list(set(train_dataset)&set(knownComplex))
        if len(share) >0:
            if knownComplex not in complexList:
                complexList.append(knownComplex)

    result_complex_path = '../dataset/temp/secondExperiments/known_complex.json'
    with open(result_complex_path, 'w') as fw:
        json.dump(complexList, fw)
    return complexList

#合并已知的和预测的复合物
def mergerComplex(parent_path, knownComplex):
    fileComplex = os.path.join(parent_path, r'dataset\temp\secondExperiments\train_COVID_resultComplexName.json')
    with open(fileComplex, 'r') as complex_fr:
        complexlines = complex_fr.readlines()
        complexJson = json.loads(complexlines[0])

    allComplexJson = {}
    num = 0
    for i in range(len(knownComplex)):
        allComplexJson[num] = knownComplex[i]
        num += 1

    for complex in complexJson.values():
        allComplexJson[num] = complex
        num += 1

    result_allcomplex_path = '../dataset/temp/secondExperiments/allComplex.json'
    with open(result_allcomplex_path, 'w') as fw:
        json.dump(allComplexJson, fw)

if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    complex_json_data = readknownComplex(parent_path)
    knownComplex = readknownpro(parent_path, complex_json_data)
    mergerComplex(parent_path, knownComplex)