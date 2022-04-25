#在获取核心蛋白质前获取种子节点
import os.path
import numpy as np
import networkx as nx
import pandas as pd
from numpy import *

#基于所有节点构图
def getGraph(parent_path):
    sim_path = os.path.join(parent_path, r'dataset\secondExperiments\train_COVID_AllHuman_GoSim.xls')#蛋白质互作网络
    every_pro_path = os.path.join(parent_path, r'dataset\secondExperiments\COVID_Node2Vec.csv')#拿到由node2vec方法生成的向量数据
    G = nx.Graph()
    pro_file = pd.read_csv(every_pro_path)
    pro = np.array(pro_file["name"])
    for i in range(len(pro)):
        G.add_node(pro[i])

    edges_df = pd.read_excel(sim_path)
    source = np.array(edges_df["protein"])
    target = np.array(edges_df["neghbor_protein"])
    for j in range(len(source)):
        G.add_edge(source[j].split("_")[1], target[j].split("_")[1])
    print("图形已构成")

    return G

#基于边聚类系数和度获取核心种子节点
def getSeedNodes_ECC(G):
    #bc = nx.betweenness_centrality(G)
    adj = G._adj

    NC = {}
    for u in G.nodes():
        u_adj = adj[u]
        if len(u_adj) > 1:
            u_d = G.degree(u)
            NCu = 0
            for v in u_adj.keys():
                v_d = G.degree(v)
                mind = min(u_d - 1, v_d - 1)
                v_adj = adj[v]
                Zuv = len(set(u_adj.keys()) & set(v_adj.keys()))
                if mind == 0:
                    NCu += 0
                else:
                    NCu += Zuv / mind
            NC[u] = NCu

    sub = {}
    for k in NC.keys():
        if G.degree(k) != 0 and NC[k] / G.degree(k) != 1.0:
            sub[k] = NC[k] / G.degree(k)

    subavg = mean(list(sub.values()))
    print("subavg:", subavg)
    # subavg += 0.03
    print("改变后的subavg:", subavg)
    seed = {}
    for n in sub.keys():
        avedeg = getsubgraph(n,G,adj)
        if sub[n] > subavg:
            print(n)
            seed[n] = sub[n]
    print(len(seed))

    return seed

def getsubgraph(n,G,adj):
    n_adj = adj[n]
    degsum = 0
    nodesum = 1
    for i in n_adj.keys():
        edgesum = 1
        for j in n_adj.keys():
            if i != j:
                if G.has_edge(i,j):
                    edgesum += 1
        if edgesum > 1:
            degsum += edgesum
            nodesum += 1
    degsum += nodesum - 1
    avedeg = degsum/nodesum

    return avedeg


def getSeedProVec(parent_path, seed):
    raw_dataset_path = os.path.join(parent_path, r'minmax_out\secondExperiments\raw_minmax.out')
    seed_dataset_path = os.path.join(parent_path, r'minmax_out\secondExperiments\seed_minmax.out')
    every_pro_path = os.path.join(parent_path, r'dataset\secondExperiments\COVID_Node2Vec.csv')
    pro_file = pd.read_csv(every_pro_path)
    pro = np.array(pro_file["name"])

    raw_dataset = np.loadtxt(raw_dataset_path, delimiter = ',')
    m, n = raw_dataset.shape
    matrix = np.zeros((len(seed), n))
    i = 0
    for k,v in seed.items():
        index = np.where(pro == k)[0][0]
        matrix[i, 0:n] = raw_dataset[index, 0:n]
        # matrix[i,0:n-1] = raw_dataset[index,0:n-1]
        # matrix[i,n-1] = v
        i += 1
    # for i in range(len(seed)):
    #     index = np.where(pro == seed[i])[0][0]
    #     matrix[i] = raw_dataset[index]
    np.savetxt(seed_dataset_path, matrix, delimiter=',', fmt='%s')

if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    graph = getGraph(parent_path)
    seed = getSeedNodes_ECC(graph)
    getSeedProVec(parent_path, seed)

    #获取种子节点后将NC值作为分数值带入到聚类中，按照分数值来选择中心点