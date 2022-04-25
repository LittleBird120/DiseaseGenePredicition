#-*- codeing=utf-8 -*-
#@Time:2022/4/13 15:57
#@Author:夏生荣
#@File:getMethodPrecision.py
#@software:PyCharm
import  os
from sklearn import preprocessing
import numpy as np
import string

path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
filePathogenic = path + "/dataset/result/allSimilarity.txt"
file = path + "/dataset/uploads/secondExperiments/train.txt"

proteins = []
protein_similarity=[]
knownFactors=[]
with open(filePathogenic, 'r') as Pathogenic_fr:
    pathogenic = Pathogenic_fr.read()
    list = pathogenic.split("\n")#数组
    for item in list:
        p = item[0:6]
        s = item[7:].strip()
        if p not in proteins:
            proteins.append(p)
            protein_similarity.append(s)
print(proteins.__len__())
print(protein_similarity)
print(protein_similarity.__len__())

with open(file, 'r') as fr:
    pat = fr.read()
    list = pat.split("\n")#数组
    for item in list:
        p = item[0:6]
        if p not in knownFactors:
            knownFactors.append(p)
print(knownFactors.__len__())

res_list =[]
for item in knownFactors:
    if item in proteins:
        res_list.append(item)
print(res_list)
print(res_list.__len__())


test = []
# print(protein_similarity.__len__())
res_index=[]
for item in protein_similarity:
    list=[]
    if item.__len__() < 1:
        break;
    num = float(item)
    list.append(num)
    test.append(list)
# print(test)
X = np.array(test)
min_max_scaler = preprocessing.MinMaxScaler()
X_minMax = min_max_scaler.fit_transform(X)
# print(X_minMax)
for i in range(X_minMax.__len__()):
    if X_minMax[i]>0.1:
        res_index.append(i)
# print(res_index.__len__())
res_arr = []
for item in res_index:
    res_arr.append(proteins[item])
print(res_arr)
print(res_arr.__len__())