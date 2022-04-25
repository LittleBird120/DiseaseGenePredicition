import os
import math
import json
import pandas as pd
import numpy as np

def readpro(parent_path):
    # every_pro_path = os.path.join(parent_path, r'dataset\DIPHumanOntology.xls')
    every_pro_path = os.path.join(parent_path, r'dataset\secondExperiments\COVID_Node2Vec.csv')
    # pro_file = pd.read_excel(every_pro_path)
    pro_file = pd.read_csv(every_pro_path)
    # pro = np.array(pro_file["protein"])
    pro = np.array(pro_file["name"])
    return pro

def readresultjson(parent_path,protein):
    # result_corefile = os.path.join(parent_path, r'result\DIP_AllHuman_resultComplex.json')
    result_corefile = os.path.join(parent_path,r'result\secondExperiments\train_COVID_resultComplex.json')
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

    pronum = list(set(pronum))
    print("种子数为："+str(len(pronum)))

    return predictJson

def readknown(parent_path):
    knownpro_file = os.path.join(parent_path, r'dataset\humanComplex.json')
    with open(knownpro_file, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
    return json_data

def calculateAvgSize(predictdata):
    dataNum = len(predictdata)
    num = 0
    for k, cluster in predictdata.items():
        num += len(cluster)
    num = num/dataNum
    print("复合物平均大小为："+str(num))

def overlap_ratio(predictdata,knowndata):
    goNetwork_dict = {}
    for k,cluster in predictdata.items():
        list_goNetwork = []
        for i in range(len(knowndata)):
            knownlist = knowndata[i]["subunits(UniProt IDs)"].split(";")
            share = [x for x in cluster if (x in knownlist)]
            o = len(share)  # 共有的蛋白质的个数
            c1 = len(cluster)  # 预测的团的蛋白质个数
            c2 = len(knownlist)  # 基准复合物的蛋白质个数
            if o == c1 == c2 and o > 3:
                print(cluster)
            # Or = round((2 * o) / (c1 + c2), 2)
            Or = (math.pow(o,2))/(c1*c2)
            list_goNetwork.append(Or)
        or_goNetwork = max(list_goNetwork)
        goNetwork_dict[k] = or_goNetwork
    return goNetwork_dict

def compare_precision(goNetwork_dict):
    num = 0
    for k,v in goNetwork_dict.items():
        # if v >= 0.2:
        if v >= 0.02:
            num += 1
    precision = num/len(goNetwork_dict)
    print("准确率："+str(precision))

    return precision

def compare_recall(predictdata,knowndata):
    goNetwork_dict = {}
    for i in range(len(knowndata)):
        knownlist = knowndata[i]["subunits(UniProt IDs)"].split(";")
        list_goNetwork = []
        for k, cluster in predictdata.items():
            share = [x for x in knownlist if (x in cluster)]
            o = len(share)  # 共有的蛋白质的个数
            c1 = len(cluster)  # 预测的团的蛋白质个数
            c2 = len(knownlist)  # 基准复合物的蛋白质个数
            Or = (math.pow(o,2))/(c1*c2)
            list_goNetwork.append(Or)
        or_goNetwork = max(list_goNetwork)
        goNetwork_dict[i] = or_goNetwork

    num = 0
    for k, v in goNetwork_dict.items():
        # if v >= 0.2:
        if v >= 0.02:
            num += 1
    recall = num / len(knowndata)
    print("召回率：" + str(recall))

    return recall

def compare_F_measure(precision,recall):
    f_score = 2*precision*recall/(precision+recall)
    print("f值：" + str(f_score))

def compare_Sn(predictdata,knowndata):
    sumT_max = 0
    sumNi = 0
    for i in range(len(knowndata)):
        knownlist = knowndata[i]["subunits(UniProt IDs)"].split(";")
        T_max = 0
        for k, cluster in predictdata.items():
            share = [x for x in knownlist if (x in cluster)]
            if len(share) >= T_max:
                T_max = len(share)
        sumT_max += T_max
        sumNi += len(knownlist)
    Sn = sumT_max/sumNi
    print("敏感度为：" + str(Sn))
    return Sn

def compare_PPV(predictdata, knowndata):
    sumT_max = 0
    summTij = 0
    for k,cluster in predictdata.items():
        T_max = 0
        sumnTij = 0
        for i in range(len(knowndata)):
            knownlist = knowndata[i]["subunits(UniProt IDs)"].split(";")
            share = [x for x in cluster if (x in knownlist)]
            sumnTij += len(share)
            if len(share) >= T_max:
                T_max = len(share)
        sumT_max += T_max
        summTij += sumnTij
    PPV = sumT_max / summTij
    print("阳性预测值为：" + str(PPV))
    return PPV

def compare_Acc(Sn, PPV):
    acc = math.sqrt(Sn*PPV)
    print("准确性为：" + str(acc))
    return acc

if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    protein = readpro(parent_path)
    predictdata = readresultjson(parent_path,protein)
    knowndata = readknown(parent_path)
    calculateAvgSize(predictdata)
    goNetwork_dict = overlap_ratio(predictdata,knowndata)
    precision = compare_precision(goNetwork_dict)
    recall = compare_recall(predictdata,knowndata)
    compare_F_measure(precision,recall)
    Sn = compare_Sn(predictdata,knowndata)
    PPV = compare_PPV(predictdata, knowndata)
    compare_Acc(Sn, PPV)