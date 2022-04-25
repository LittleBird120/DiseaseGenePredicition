import os
import math
import json
import pandas as pd
import numpy as np

def readpro(parent_path):
    every_pro_path = os.path.join(parent_path, r'dataset\secondExperiments\COVID_Node2Vec.csv')
    pro_file = pd.read_csv(every_pro_path)
    pro = np.array(pro_file["name"])

    return pro

def readresultjson(parent_path,protein):
    result_corefile = os.path.join(parent_path, r'result\secondExperiments\train_COVID_resultComplex.json')
    with open(result_corefile, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)

    predictJson = {}
    pronum = []
    for k,v in json_data.items():
        cover = []
        cluster = v[0]["cover"]
        pronum.extend(cluster)
        for i in cluster:
            cover.append(protein[int(i)])
        predictJson[k] = cover
        # if v[0]["score"] >= 0.5:
        #     predictJson[k] = [{"score":v[0]["score"],"cover":cover}]

    return predictJson

def savecomplex(parent_path,complexjson):
    result_path = parent_path + r'\result\secondExperiments\train_COVID_resultComplexName.json'  #获取的是评分大于0.5的复合物
    with open(result_path, 'w') as fw:
        json.dump(complexjson, fw)

if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    protein = readpro(parent_path)
    predictdata = readresultjson(parent_path,protein)
    savecomplex(parent_path, predictdata)