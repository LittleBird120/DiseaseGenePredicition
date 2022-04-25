#给定两个基因，如果它们存在于Ｍ个相同的蛋白质复合物中，则共有的M数就是这两个基因之间的相似度
import pandas as pd
import numpy as np
import json
import os
import math
import time
import networkx as nx
from collections import OrderedDict

#计算每个复合物中已知宿主蛋白的比例
def getComplexKnownHostProProportion(fileComplex,filePathogenic):
    with open(fileComplex, 'r') as complex_fr:
        complexlines = complex_fr.readlines()
        complexJson = json.loads(complexlines[0],object_pairs_hook=OrderedDict)

    with open(filePathogenic, 'r') as Pathogenic_fr:
        pathogenic = Pathogenic_fr.readlines()
    hostPro = [i.strip("\n") for i in pathogenic]

    num = 0
    complex_hostProProportion = []
    for complex in complexJson.values():
        share = list(set(complex) & set(hostPro))
        n = len(share)
        if n != 0:
            w = n / len(complex)
            if len(share) >= 2:
                num += 1
            complex_hostProProportion.append({"cover": complex, "w": w, "common":share})
    print("包含超过2个已知宿主蛋白的复合物个数为"+str(num))
    return complex_hostProProportion, hostPro

#获取所有节点的向量表示形式
def getNodeVector(fileEMB, raw_dataset_path):
    nodeVecDict = {}
    raw_dataset = np.loadtxt(raw_dataset_path, delimiter=',')
    m, n = raw_dataset.shape
    pro_file = pd.read_csv(fileEMB)
    pro = np.array(pro_file["name"])
    vec = np.array(pro_file["node2vec"])

    for i in range(len(pro)):
        every_nodeVecList = []
        node_vector_list = raw_dataset[i, 0:n-2]
        for j in range(len(node_vector_list)):
            every_nodeVecList.append(float(node_vector_list[j]))
        nodeVecDict[pro[i]] = every_nodeVecList

    # for i in range(len(pro)):
    #     every_nodeVecList = []
    #     node_vector_list = vec[i].strip("\n").strip("[").strip("]").split(", ")
    #     for j in range(len(node_vector_list)):
    #         every_nodeVecList.append(float(node_vector_list[j]))
    #     nodeVecDict[pro[i]] = every_nodeVecList
    return nodeVecDict

#找出每个候选蛋白对应的最大的复合物
def getComplex_candidatePro(complex_hostProProportion,fileCandidate):
    with open(fileCandidate, 'r') as f2:
        candidate = f2.readlines()

    candidate_complex_huge = {}
    for node in candidate:
        every_candidate = node.split("\t")[0]
        proportion = 0
        candidate_complex = []
        share_complex = []
        for i in range(len(complex_hostProProportion)):
            if every_candidate in complex_hostProProportion[i]["cover"]:
                if complex_hostProProportion[i]["w"] >= proportion:
                    proportion = complex_hostProProportion[i]["w"]
                    candidate_complex = complex_hostProProportion[i]["cover"]
                    share_complex = complex_hostProProportion[i]["common"]
        if len(candidate_complex) != 0:
            candidate_complex_huge[every_candidate] = [{"cover": candidate_complex, "w": proportion, "common":share_complex}]
    result_host_path = '../dataset/result/all_candidate_complex_huge.json'
    with open(result_host_path, 'w') as fw:
        json.dump(candidate_complex_huge, fw)
    return candidate_complex_huge

# #计算复合物相似度
# def similarity_complex(candidate_complex_huge):
#     simAllDict = {}
#     for candidate, value in candidate_complex_huge.items():
#         # simVec = 0
#         # common = value[0]["common"]
#         # for node in common:
#         #     simVec += math.sqrt(sum([(a - b) ** 2 for (a, b) in zip(nodeVecDict[node], nodeVecDict[candidate])]))
#         sim = value[0]["w"]
#         simAllDict[candidate] = sim
#     simAllDict = sorted(simAllDict.items(), key=lambda item: item[1], reverse=True)
#
#     fileSim = "../dataset/result/complexSimilarity.txt"
#     with open(fileSim, "w") as fw:
#         for j in range(len(simAllDict)):
#             fw.write(simAllDict[j][0] + "\t" + str(simAllDict[j][1]) + "\n")
#     fw.close()
#     return simAllDict
#
# #计算node2vec相似度
# def similarity_node2vec(candidate_complex_huge, nodeVecDict, hostPro):
#     simAllDict = {}
#     for candidate, value in candidate_complex_huge.items():
#         simCalcute = []
#         for node in hostPro:
#             simVec = math.sqrt(sum([(a - b) ** 2 for (a, b) in zip(nodeVecDict[node], nodeVecDict[candidate])]))
#             simCalcute.append(simVec)
#         maxSim = max(simCalcute)
#         sim = maxSim
#         simAllDict[candidate] = sim
#     simAllDict = sorted(simAllDict.items(), key=lambda item: item[1], reverse=True)
#
#     fileSim = "../dataset/result/node2vecSimilarity.txt"
#     with open(fileSim, "w") as fw:
#         for j in range(len(simAllDict)):
#             fw.write(simAllDict[j][0] + "\t" + str(simAllDict[j][1]) + "\n")
#     fw.close()
#     return simAllDict
#
# def similarity(simComplex, simNode2vec):
#     simComplex = dict(simComplex)
#     simNode2vec = dict(simNode2vec)
#     simAllDict = {}
#     for node, sim in simComplex.items():
#         simAllDict[node] = sim+simNode2vec[node]
#     simAllDict = sorted(simAllDict.items(), key=lambda item: item[1], reverse=True)
#     save(simAllDict)

def similarity(candidate_complex_huge, nodeVecDict):
    simAllDict = {}
    for candidate, value in candidate_complex_huge.items():
        simVec = 0
        common = value[0]["common"]
        for node in common:
            simVec += math.sqrt(sum([(a - b) ** 2 for (a, b) in zip(nodeVecDict[node], nodeVecDict[candidate])]))
        sim = value[0]["w"]*simVec
        simAllDict[candidate] = sim
    simAllDict = sorted(simAllDict.items(), key=lambda item: item[1], reverse=True)

    save(simAllDict)

def save(simAllDict):
    fileSim = "../dataset/result/allSimilarity.txt"
    with open(fileSim, "w") as fw:
        for j in range(len(simAllDict)):
            fw.write(simAllDict[j][0] + "\t" + str(simAllDict[j][1]) + "\n")
    fw.close()

if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    fileComplex = path + "/dataset/temp/secondExperiments/allComplex.json"
    filePathogenic = path + "/dataset/uploads/secondExperiments/train.txt"  #已知宿主蛋白
    fileCandidate = path + "/dataset/uploads/secondExperiments/candidateNode_degree.txt"  #候选宿主蛋白
    fileEMB = path + "/dataset/temp/secondExperiments/COVID_Node2Vec.csv"
    raw_dataset_path = path + '/dataset/minmax_out/secondExperiments/raw_minmax.out'
    complex_hostProProportion, hostPro = getComplexKnownHostProProportion(fileComplex,filePathogenic)
    nodeVecDict = getNodeVector(fileEMB, raw_dataset_path)
    candidate_complex_huge = getComplex_candidatePro(complex_hostProProportion, fileCandidate)
    similarity(candidate_complex_huge, nodeVecDict)
    # simComplex = similarity_complex(candidate_complex_huge)
    # simNode2vec = similarity_node2vec(candidate_complex_huge, nodeVecDict, hostPro)
    # similarity(simComplex, simNode2vec)