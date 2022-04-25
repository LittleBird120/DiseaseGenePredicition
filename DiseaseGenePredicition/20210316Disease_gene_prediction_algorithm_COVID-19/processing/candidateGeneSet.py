import os
import json
import pandas as pd
import numpy as np
import networkx as nx

#所有节点和边构成网络图
def form_graph(parent_path):
    every_pro_path = os.path.join(parent_path, r'dataset\temp\secondExperiments\COVID_Node2Vec.csv')
    simGO_path = os.path.join(parent_path, r'dataset\temp\secondExperiments\train_COVID_AllHuman_GoSim.xls')

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

    nodeDegree = G.degree()
    return G, nodeDegree

#候选基因集节点映射
def nodeMapping(degrees):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    node_degreename = path + '/dataset/uploads/secondExperiments/candidateNode_degree.txt'
    filePathogenic = path + "/dataset/uploads/secondExperiments/train.txt"  # 已知宿主蛋白

    with open(filePathogenic, 'r') as Pathogenic_fr:
        pathogenic = Pathogenic_fr.readlines()
    hostPro = [i.strip("\n") for i in pathogenic]

    with open(node_degreename, "w") as fw:
        for node in degrees:
            if node[1] >= 15:
                fw.write(node[0])
                fw.write("\t")
                fw.write(str(node[1]))
                fw.write("\n")
    # candidateNode = {}
    # for node in degrees:
    #     if node[0] not in hostPro and node[1] >= 15:
    #         candidateNode[node[0]] = node[1]
    # return candidateNode

def saveCandidate(candidateNode):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    node_degreename = path + '/dataset/uploads/secondExperiments/candidateNode_degree.txt'
    filePathogenic = path + "/dataset/uploads/secondExperiments/test.txt"  # 已知宿主蛋白

    with open(filePathogenic, 'r') as Pathogenic_fr:
        pathogenic = Pathogenic_fr.readlines()
    hostPro = [i.strip("\n") for i in pathogenic]

    nodeDict = {}
    num = 0
    num2 = 0
    with open(node_degreename, "w") as fw:
        for node, degree in candidateNode.items():
            if node in hostPro:
                fw.write(node)
                fw.write("\t")
                fw.write(str(degree))
                fw.write("\n")
                num += 1
            else:
                nodeDict[node] = degree
        for k,v in nodeDict.items():
            if num2 <= num:
                fw.write(k)
                fw.write("\t")
                fw.write(str(v))
                fw.write("\n")
                num2 += 1

if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    graph, nodeDegree = form_graph(parent_path)
    nodeMapping(nodeDegree)
    # candidateNode = nodeMapping(nodeDegree)
    # saveCandidate(candidateNode)
