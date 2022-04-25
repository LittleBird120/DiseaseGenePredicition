import os
import json
import pandas as pd
import numpy as np
import networkx as nx

#所有节点和边构成网络图
def form_graph(parent_path):
    every_pro_path = os.path.join(parent_path, r'dataset\secondExperiments\COVID_Node2Vec.csv')
    simGO_path = os.path.join(parent_path, r'dataset\secondExperiments\train_COVID_AllHuman_GoSim.xls')

    # 网络图的构建
    G = nx.Graph()
    pro_file = pd.read_csv(every_pro_path)
    pro = np.array(pro_file["name"])
    proList = []  # 每个蛋白质的索引
    for i in range(len(pro)):
        proList.append(pro[i])
        G.add_node(i)

    edges_df = pd.read_excel(simGO_path)
    source = np.array(edges_df["protein"])
    target = np.array(edges_df["neghbor_protein"])
    sim = np.array(edges_df["sim"])
    edgesList = []
    for j in range(len(source)):
        edgesList.append((source[j].split("_")[1], target[j].split("_")[1]))
        G.add_edge(int(source[j].split("_")[0]), int(target[j].split("_")[0]))
        G[int(source[j].split("_")[0])][int(target[j].split("_")[0])]['weight'] = sim[j]
    print("图形已构成")
    return G

#通过所有核数据
def readresultjson(parent_path, graph):
    result_corefile = os.path.join(parent_path, r'result\secondExperiments\train_COVID_result.json')
    with open(result_corefile, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)

    seed = []
    for core_k, core_v in json_data.items():
        core = core_v[0]["cover"]
        seed.extend(core)
    seed = list(set(seed))
    return json_data,seed

#通过核获得一阶邻点
def getfirstneighbor(json_data,seed,graph):
    adj = graph._adj
    neighbordict = {}
    for k,v in json_data.items():
        allneighborNode = []
        neighborNode = []
        core = v[0]["cover"]
        for i in core:
            everyneigh = adj[int(i)].keys()
            neighborNode.extend(everyneigh)
        neighborNode = list(set(neighborNode))
        for i in neighborNode:
            if i not in seed:
                allneighborNode.append(i)
        neighbordict[k] = neighborNode
    return adj,neighbordict

#适应度函数
def fitness_function(adj,complex, core,graph):
    sum_degree_in = 0  # 所有顶点的入度之和
    sum_degree_out = 0  # 所有顶点的出度之和
    E = 0
    for i in range(len(complex)):
        degree_in = 0  # 每个节点的入度
        degree_out = 0  # 每个节点的出度
        i_adj = adj[complex[i]].keys()
        for z in i_adj:
            if z in complex:
                if (complex[i], int(z)) in graph.edges():
                    degree_in += graph[complex[i]][int(z)]['weight']
                else:
                    degree_in += graph[int(z)][complex[i]]['weight']
            else:
                if (complex[i], int(z)) in graph.edges():
                    degree_out += graph[complex[i]][int(z)]['weight']
                else:
                    degree_out += graph[int(z)][complex[i]]['weight']
        for j in range(len(complex)):
            if i < j:
                if (complex[i], complex[j]) in graph.edges() or (
                complex[j], complex[i]) in graph.edges():
                    E += 1
        sum_degree_in += degree_in
        sum_degree_out += degree_out
    a = 0.8
    modularity = (sum_degree_in - sum_degree_out) / (sum_degree_out + sum_degree_in)
    density = (2 * E) / (len(complex) * (len(complex) - 1))
    score = a*density+(1-a)*modularity
    return score

#通过分数形成核心-附件的形式
def core_accessories(json_data,neighbordict,adj,graph):
    resultDict = {}
    for k, v in json_data.items():
        complexjson = {}
        resultList = []
        core = [int(i) for i in v[0]["cover"]]
        complex = core+neighbordict[k]
        #求每个一阶邻点与core总的功能相似性
        score_neighbordict = {}
        for j in neighbordict[k]:
            score = 0
            for z in core:
                if (int(z), int(j)) in graph.edges():
                    score += graph[int(z)][int(j)]['weight']
                elif (int(j), int(z)) in graph.edges():
                    score += graph[int(j)][int(z)]['weight']
                else:
                    score += 0
            score_neighbordict[j] = score
        score_neighbordict = sorted(score_neighbordict.items(), key=lambda item: item[1])

        if len(complex) > 3:
            core_score = fitness_function(adj, complex, core, graph)
            for i in score_neighbordict:
                # for i in neighbordict[k]:
                if len(complex) > 3:
                    complex.remove(i[0])
                    complex_score = fitness_function(adj, complex, core, graph)
                    if complex_score >= core_score:
                        core_score = complex_score
                    else:
                        complex.append(i[0])
                else:
                    break

        elif len(complex) == 3:
            core_score = fitness_function(adj, complex, core, graph)
        else:
            # continue
            core_score = 0


        # if len(core) > 1:
        #     core_score = fitness_function(adj,core)
        # else:
        #     core_score = 0
        # complex = core
        # for i in neighbordict[k]:
        #     complex.append(i)
        #     complex_score = fitness_function(adj, complex)
        #     if complex_score >= core_score:
        #         core_score = complex_score
        #     else:
        #         complex.remove(i)
        complexjson["cover"] = complex
        complexjson["score"] = core_score
        resultList.append(complexjson)
        resultDict[k] = resultList
    return resultDict

def savecomplex(parent_path,complexjson):
    result_path = parent_path + r'\result\secondExperiments\train_COVID_resultComplex.json'
    with open(result_path, 'w') as fw:
        json.dump(complexjson, fw)

if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    graph = form_graph(parent_path)
    json_data,seed = readresultjson(parent_path, graph)
    adj,neighbordict = getfirstneighbor(json_data,seed,graph)
    complexjson = core_accessories(json_data,neighbordict,adj,graph)
    print(complexjson.__len__())
    savecomplex(parent_path,complexjson)