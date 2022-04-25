#通过node2vec算法获取的节点向量表示计算相似度
import math
import os
import time
import pandas as pd
import numpy as np

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
        node_vector_list = raw_dataset[i, 0:n - 2]
        for j in range(len(node_vector_list)):
            every_nodeVecList.append(float(node_vector_list[j]))
        nodeVecDict[pro[i]] = every_nodeVecList
    return nodeVecDict

def caculateNodeVecSim(nodeVecDict,path):
    NodeVecSimDict = {}
    filePathogenic = path + "/dataset/uploads/train.txt"  # 已知宿主蛋白
    fileCandidate = path + "/dataset/uploads/candidateNode_degree.txt"  # 候选宿主蛋白
    with open(filePathogenic, 'r') as f1:
        pathogenic = f1.readlines()

    with open(fileCandidate, 'r') as f2:
        candidate = f2.readlines()

    for i in candidate:
        simCalcute = []
        every_candidate = i.split("\t")[0]
        for every_pathogenic in pathogenic:
            every_pathogenic = every_pathogenic.strip("\n")
            sim = math.sqrt(sum([(a - b) ** 2 for (a, b) in zip(nodeVecDict[every_candidate], nodeVecDict[every_pathogenic])]))
            simCalcute.append(sim)
        maxSim = max(simCalcute)
        print(maxSim)
        NodeVecSimDict[every_candidate] = maxSim
    return NodeVecSimDict

def save(NodeVecSimDict):
    fileSim = "../dataset/result/Candidate_NodeVecSim.txt"
    with open(fileSim, "w") as fw:
        for key, value in NodeVecSimDict.items():
            fw.write(key + "\t" + str(value) + "\n")
    fw.close()

if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    NodeVecTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("开始获取节点的向量表示：" + NodeVecTime)
    fileEMB = path + "/dataset/temp/COVID_Node2Vec.csv"
    raw_dataset_path = path + '/dataset/minmax_out/raw_minmax.out'
    nodeVecDict = getNodeVector(fileEMB, raw_dataset_path)

    simNodeVecTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("基于向量表示开始计算相似度：" + simNodeVecTime)
    NodeVecSimDict = caculateNodeVecSim(nodeVecDict,path)
    save(NodeVecSimDict)