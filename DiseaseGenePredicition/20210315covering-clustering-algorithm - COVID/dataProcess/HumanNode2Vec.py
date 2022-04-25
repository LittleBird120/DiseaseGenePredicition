import pandas as pd
import numpy as np
import os.path
import networkx as nx

def get_degree(profile,every_edge_path):
    G = nx.Graph()

    pro_file = pd.read_csv(profile)
    pro = np.array(pro_file["name"])
    for i in range(len(pro)):
        G.add_node(i)

    edges_df = pd.read_excel(every_edge_path)
    source = np.array(edges_df["protein"])
    target = np.array(edges_df["neghbor_protein"])
    for j in range(len(source)):
        G.add_edge(int(source[j].split("_")[0]), int(target[j].split("_")[0]))

    degree = G.degree()
    degreeList = []
    for k in degree:
        degreeList.append(k[1])

    return degreeList

#获取Prot2Vec构成的矩阵
def get_matrix(profile,degree):
    file = pd.read_csv(profile)
    name = np.array(file["name"])
    vec = np.array(file["node2vec"])
    matrix = np.zeros((len(name), 130))
    for i in range(len(matrix)):
        vec_list = vec[i].split(',')
        for j in range(len(vec_list)):
            matrix[i, j] = float(vec_list[j].strip().strip('[]'))
            # print(float(vec_list[j].strip().strip('[]')))
        matrix[i, 128] = i
        matrix[i, 129] = degree[i]
    print(matrix)
    return matrix

def save(matrix):
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    path = os.path.join(parent_path, r'dataset\secondExperiments\protein_matrix.out')
    np.savetxt(path, matrix, delimiter=',', fmt='%s')

if __name__ == "__main__":
    profile = "../dataset/secondExperiments/COVID_Node2Vec.csv"
    every_edge_path = "../dataset/secondExperiments/train_COVID_AllHuman_GoSim.xls"
    degree = get_degree(profile,every_edge_path)
    matrix = get_matrix(profile,degree)
    save(matrix)