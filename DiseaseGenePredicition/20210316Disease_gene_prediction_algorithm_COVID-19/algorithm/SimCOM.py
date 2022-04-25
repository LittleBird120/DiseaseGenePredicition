#给定两个基因，如果它们存在于Ｍ个相同的蛋白质复合物中，则共有的M数就是这两个基因之间的相似度
import pandas as pd
import numpy as np
import json
import os
import time
import networkx as nx
from collections import OrderedDict

#所有节点和边构成网络图
def form_graph(path):
    every_pro_path = path + "/dataset/temp/COVID_Node2Vec.csv"
    simGO_path = path + "/dataset/temp/train_COVID_AllHuman_GoSim.xls"

    # 网络图的构建
    G = nx.Graph()
    pro_file = pd.read_csv(every_pro_path)
    pro = np.array(pro_file["name"])
    for i in range(len(pro)):
        G.add_node(pro[i])

    edges_df = pd.read_excel(simGO_path)
    source = np.array(edges_df["protein"])
    target = np.array(edges_df["neghbor_protein"])
    sim = np.array(edges_df["sim"])
    for j in range(len(source)):
        G.add_edge(source[j].split("_")[1], target[j].split("_")[1])
        G[source[j].split("_")[1]][target[j].split("_")[1]]['weight'] = sim[j]
    print("图形已构成")
    return G

#获取所有复合物的对应的数字标号
def getComplexNum(file,G):
    densityAll = []
    with open(file, 'r') as complex_fr:
        complexlines = complex_fr.readlines()
        complexJson = json.loads(complexlines[0],object_pairs_hook=OrderedDict)
    for complex in complexJson.values():
        density = one_complex_density(complex, G)
        densityAll.append(density)
    return densityAll,complexJson

#计算单个复合物的密度
def one_complex_density(complex,G):
    edgesList = G.edges
    edgenum = 0
    length = len(complex)
    # print(length)
    for i in range(len(complex)):
        for j in range(len(complex)):
            if i >= j:
                continue
            elif (complex[i],complex[j]) in edgesList or (complex[j],complex[i]) in edgesList:
                edgenum += 1

    density = (2*edgenum)/(length*(length-1))
    return density

#计算候选基因与致病基因之间的相似度计算
def sim(filePathogenic,fileCandidate,densityAll,complexJson):
    candidateDict = {}  #存储候选蛋白
    lines = list(complexJson.values())  #所有的复合物
    with open(filePathogenic, 'r') as f1:
        pathogenic = f1.readlines()

    with open(fileCandidate, 'r') as f2:
        candidate = f2.readlines()

    for i in candidate:
        simCalcute = 0
        every_candidate = i.split("\t")[0]
        for every_pathogenic in pathogenic:
            every_pathogenic = every_pathogenic.strip("\n")
            for z in range(len(lines)):
                lineList = lines[z]
                if every_pathogenic in lineList and every_candidate in lineList:
                    simCalcute += densityAll[z]
        print("每个候选基因" + every_candidate + "的相似度：" + str(simCalcute))
        candidateDict[every_candidate] = simCalcute
    return candidateDict

#存储相似度计算
def saveComplexSim(candidateSim):
    fileSim = "../dataset/result/Candidate_complexSim.txt"
    with open(fileSim,"w") as fw:
        for key,value in candidateSim.items():
            fw.write(key + "\t" + str(value) + "\n")
    fw.close()

if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    fileComplex = path + "/dataset/temp/train_COVID_resultComplexName.json"
    filePathogenic = path + "/dataset/uploads/train.txt"  #已知宿主蛋白
    fileCandidate = path + "/dataset/uploads/candidateNode_degree.txt"  #候选宿主蛋白

    startGraphTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("开始构图：" + startGraphTime)
    G = form_graph(path)

    startDensityTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("开始计算复合物的密度：" + startDensityTime)
    densityAll,complexJson = getComplexNum(fileComplex,G)

    simTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("开始计算相似度：" + simTime)
    candidateSim = sim(filePathogenic,fileCandidate,densityAll,complexJson)
    saveComplexSim(candidateSim)

    endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("算法结束时间：" + endTime)