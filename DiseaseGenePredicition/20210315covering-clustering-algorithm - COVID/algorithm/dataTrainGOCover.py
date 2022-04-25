#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import os.path
import numpy as np
np.set_printoptions(suppress=True)
import math
import json
import copy
import random
import networkx as nx
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import math
from collections import Counter

#得到当前目录的绝对路径
ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
parent_path  = os.path.dirname(ROOT_DIR)


# In[1]:


class DataTrain:
    # 当前迭代数
    __lter = 0
    # 训练数据目录
    __train_path = ''
    # # 相似度矩阵
    # __sim_matrix = np.zeros((27622, 3))
    #网络图
    __graph = nx.Graph()

    def __init__(self, l, p, G):
        self.__lter = l
        self.__train_path = p
        # self.__sim_matrix = sim_matrix
        self.__graph = G

    def start_train(self):
        # 计算两点之间的距离
        def eucliDist(graph, A, B, A_index, B_index):
            dis = 0
            if (int(A_index), int(B_index)) in graph.edges():
                sim = graph[int(A_index)][int(B_index)]['weight']
            elif (int(B_index), int(A_index)) in graph.edges():
                sim = graph[int(B_index)][int(A_index)]['weight']
            else:
                sim = 0
            dis = math.sqrt(sum([(a - b) ** 2 for (a, b) in zip(A, B)])) / (1+sim)
            # dis = math.sqrt(sum([(a - b) ** 2 for (a, b) in zip(A, B)]))
            return dis
            # return (math.sqrt(sum([(a - b) ** 2 for (a, b) in zip(A, B)])) * (1+sim))

        # 当所有样本都被覆盖后结束训练
        def if_finish(train):
            m, n = train.shape
            for i in range(m):
                if train[i][n - 1] == 0:
                    f = 0
                    break
            else:
                f = 1
            return f

        # 计算覆盖圆心
        def get_center(nostudy_index, graph):
            # 重心
            core = np.zeros([1, trans_notag_n])
            for i in nostudy_index:
                for j in range(trans_notag_n):
                    core[0][j] += train_notag[i][j] * train[i][n-1]
            core = core / len(nostudy_index)

            dis = 0
            key_max = 0
            for i in nostudy_index:
                if np.dot(core[0][0:trans_notag_n], train_notag[i][0:trans_notag_n]) >= dis:
                    dis = np.dot(core[0][0:trans_notag_n], train_notag[i][0:trans_notag_n])
                    key_max = i
            center = train_notag[key_max]

            return center, key_max

        # 获取节点的3阶邻居节点
        def get_adjNode(center_adjnode,sample,adj):
            neighborNode = []
            myTrainList = train[...,n-2].tolist()
            firstAdjacent = [myTrainList.index(node) for node in center_adjnode if node in myTrainList if myTrainList.index(node) in sample]
            secondAdjacent = [myTrainList.index(j) for i in firstAdjacent if adj[i].keys() != [] for j in adj[i].keys() if j in myTrainList if myTrainList.index(j) in sample]
            # secondAdjacent = list(set(secondAdjacent))
            # thirdAdjacent = [b for a in secondAdjacent if adj[a].keys() != [] for b in adj[a].keys() if b in sample]
            # thirdAdjacent = list(set(thirdAdjacent))
            neighborNode.extend(firstAdjacent)
            neighborNode.extend(secondAdjacent)
            # neighborNode.extend(thirdAdjacent)
            neighborNode = list(set(neighborNode))
            return neighborNode

        #计算各个邻居节点的距离集合
        def get_distance(sample, center, graph, key_max):
            d = [eucliDist(graph, center[0:trans_notag_n], train_notag[index][0:trans_notag_n], train[key_max][n-2], train[index][n-2]) for index in sample]
            # 获取网络图中每个节点的一阶邻居节点
            neighborNode = []
            adj = graph._adj
            center_adjnode = adj[train[key_max][n-2]].keys()
            if center_adjnode != []:
                neighborNode = get_adjNode(center_adjnode,sample,adj)
                neighborNodeIndex = [train[i][n-2] for i in neighborNode]
                print(str(key_max)+"这个节点对应的一阶邻居节点：")
                print(neighborNode)
                print(neighborNodeIndex)
            d.sort()
            return d, neighborNode


        #计算覆盖半径
        def get_weight_radius(d):
            radius = 0
            for i in d:
                radius += i
            radius = radius/len(d)
            return radius

        # 获取覆盖
        def get_covering(graph,nostudy_index,radius,neighborNode,center,key_max):
            cover = []
            for i in nostudy_index:
                dist = eucliDist(graph, train_notag[i][0:trans_notag_n], center[0:trans_notag_n], train[i][n-2], train[key_max][n-2])
                # 节点既要小于半径同时也要是n<=2阶节点
                if dist <= radius:
                    cover.append(i)
            return cover

        # 获取矩阵B（Bij=Aij−kikj/2m）
        def get_B_matrix(cover):
            g = nx.Graph()
            edges = graph.edges()
            myTrainList = train[..., n - 2].tolist()

            # 总边数
            m = len(edges)
            # 任意两点连接边数的期望值
            Eij = np.zeros((len(cover), len(cover)))

            i = 0
            for source in cover:
                ki = train[source][n - 1]
                j = 0
                for target in cover:
                    kj = train[target][n - 1]
                    Eij[i,j] = (ki*kj)/(2*m)
                    if source <= target:
                        if (train[source][n-2], train[target][n-2]) in edges:
                            g.add_edge(source, target)
                    else:
                        if (train[target][n-2], train[source][n-2]) in edges:
                            g.add_edge(target, source)
                    j += 1
                i += 1
                g.add_node(source)
            # adj_matrix = nx.adjacency_matrix(g).todense()
            # adj_matrix = np.array(adj_matrix)
            #
            # # 节点v和w的实际边数与随机网络下边数期望之差
            # B = adj_matrix - Eij
            return g

        # 定义节点_社区矩阵
        def get_matrix(cover):
            S = np.zeros((len(cover), 1))
            for i in range(len(S)):
                S[i, 0] = 1
            return S

        #计算模块度
        def getQ(B, cluster):
            # 获取节点、社区矩阵
            node_cluster = np.dot(cluster, np.transpose(cluster))
            results = np.dot(B, node_cluster)
            # 求和
            sum_results = np.trace(results)
            # 模块度计算
            Q = sum_results / (2 * m)
            print("Q:", Q)
            return Q

        # 计算模块密度
        def get_density(g):
            nodes = len(g.nodes())
            edges = len(g.edges())
            desity = (2*edges)/(nodes*(nodes-1))
            print("desity:", desity)
            return desity



        #获取球形覆盖的圆心
        def get_centroid(cover_form):
            # 重心
            cover_core = np.zeros([1, trans_notag_n])
            for i in cover_form:
                for j in range(trans_notag_n):
                    cover_core[0][j] += train_notag[i][j] * train[i][n-1]
            cover_core = cover_core / len(cover_form)

            cover_dis = 0
            cover_key_max = 0
            for i in cover_form:
                if np.dot(cover_core[0][0:trans_notag_n], train_notag[i][0:trans_notag_n]) >= cover_dis:
                    cover_dis = np.dot(cover_core[0][0:trans_notag_n], train_notag[i][0:trans_notag_n])
                    cover_key_max = i
            cover_center = train_notag[cover_key_max]

            return cover_center, cover_key_max

        #Step1 加载训练集
        train = np.loadtxt(self.__train_path, delimiter=',')
        m, n = train.shape
        graph = self.__graph

        #Step2 将数据去除分类标签
        train_notag = train[...,0:n-2]
        notag_m ,notag_n = train_notag.shape

        di = []
        for i in range(notag_m):
            temp = 0
            for j in range(notag_n):
                temp = temp + math.pow(train_notag[i][j], 2)
            di.append(math.sqrt(temp))

        #Step3 核函数升维使其线性可分
        dmax = math.ceil(max(di))
        for i in range(len(di)):
            di[i] = math.sqrt(math.pow(dmax, 2) - math.pow(di[i], 2))
        train_notag = np.insert(train_notag, 4, di, axis=1)
        trans_notag_m, trans_notag_n = train_notag.shape

        # Step4 最后一列记为是否已学习
        haveLearned = np.zeros((trans_notag_m, 1))
        train_notag = np.concatenate((train_notag, haveLearned), axis=1)

        # Step5 开始训练
        cc = 0
        iterNum = 1  #类别数
        resultDict = {}
        while if_finish(train_notag) == 0:
            if cc == 5000:
                print('///////////////////////////////超时！/////////////////////////////////')
                break

            starttime = datetime.datetime.now()
            print("开始时间：")
            print(starttime)
            #获取未学习的样本点集合,未学习样本的索引
            result = {}
            resultList = []
            nostudy_index = [i for i in range(trans_notag_m) if train_notag[i][trans_notag_n] == 0]

            #计算圆心
            center, key_max = get_center(nostudy_index, graph)

            #计算n<=3阶邻居节点排序后的距离集合D
            d, neighborNode = get_distance(nostudy_index, center, graph, key_max)

            #计算半径
            radius = get_weight_radius(d)

            #计算覆盖样本
            cover_form = get_covering(graph,nostudy_index,radius,neighborNode,center,key_max)

            #计算覆盖后的圆心
            cover_center, cover_key_max = get_centroid(cover_form)

            cover_d, cover_neighborNode = get_distance(nostudy_index, cover_center, graph, cover_key_max)

            cover_radius = get_weight_radius(cover_d)

            cover_last = get_covering(graph, nostudy_index, cover_radius, cover_neighborNode, cover_center, cover_key_max)

            while len(cover_last) != len(cover_form):
                cover_form = cover_last
                cover_center, cover_key_max = get_centroid(cover_form)
                cover_d, cover_neighborNode = get_distance(nostudy_index, cover_center, graph, cover_key_max)
                cover_radius = get_weight_radius(cover_d)
                cover_last = get_covering(graph, nostudy_index, cover_radius, cover_neighborNode, cover_center,
                                          cover_key_max)

            cover_last.append(cover_key_max)

            neighbor_cover_last = [cover_key_max]
            for i in cover_last:
                if i in cover_neighborNode:
                    neighbor_cover_last.append(i)
            cover_last = neighbor_cover_last
            cover_last = list(set(cover_last))
            print("每次迭代获取的结果：")
            print(cover_last)

            adj = graph._adj
            center_adjnode = adj[train[cover_key_max][n - 2]].keys()
            firstadj = [x for x in cover_last if train[x][n - 2] in center_adjnode]
            if len(cover_last) > 3:
                reduce_cover_last = cover_last
                g = get_B_matrix(reduce_cover_last)
                density = get_density(g)
                sim_cover = {}
                for j in cover_last:
                    if j != cover_key_max:
                        if (int(train[j][n - 2]), int(train[cover_key_max][n - 2])) in graph.edges():
                            sim = 1 + graph[int(train[j][n - 2])][int(train[cover_key_max][n - 2])]['weight']
                        elif (int(train[cover_key_max][n - 2]), int(train[j][n - 2])) in graph.edges():
                            sim = 1 + graph[int(train[cover_key_max][n - 2])][int(train[j][n - 2])]['weight']
                        else:
                            for r in firstadj:
                                if (int(train[j][n - 2]), int(train[r][n - 2])) in graph.edges():
                                    sim = graph[int(train[j][n - 2])][int(train[r][n - 2])]['weight']
                                elif (int(train[r][n - 2]), int(train[j][n - 2])) in graph.edges():
                                    sim = graph[int(train[r][n - 2])][int(train[j][n - 2])]['weight']
                                else:
                                    sim = 0
                        sim_cover[j] = sim
                sim_cover = sorted(sim_cover.items(), key=lambda item: item[1])

                for value in sim_cover:
                    if density >= 0.6:
                        break
                    else:
                        reduce_cover_last.remove(value[0])
                        g = get_B_matrix(reduce_cover_last)
                        if get_density(g) > density:
                            density = get_density(g)
                        else:
                            reduce_cover_last.append(value[0])

                # for i in cover_last:
                #     if i != cover_key_max:
                #         reduce_cover_last.remove(i)
                #         g = get_B_matrix(reduce_cover_last)
                #         if get_density(g) > density:
                #             density = get_density(g)
                #         else:
                #             reduce_cover_last.append(i)

                cover_last = reduce_cover_last
                cover_last = list(set(cover_last))
                print("每次迭代获取的结果：")
                print(cover_last)

            if len(cover_last) != 1:
                g = get_B_matrix(cover_last)
                density = get_density(g)
                print("最终核密度：" + str(density))

            cluster = []
            for index in cover_last:
                cluster.append(train[index][n - 2])
            print("复合物核心的确定：")
            print(cluster)

            result['d'] = cover_radius
            result['w'] = cover_center.tolist()
            result['cover'] = cluster
            result['cover_key_max'] = train[cover_key_max][n - 2]
            resultList.append(result)
            resultDict[str(iterNum)] = resultList

            cc = cc + 1
            iterNum += 1
            print("类别数：")
            print(iterNum)

            for i in cover_last:
                train_notag[i][trans_notag_n] = 1

        endtime = datetime.datetime.now()
        print("结束时间：")
        print(endtime)

        #将未聚合的数据存入文本中
        result_path1 = parent_path + r'\result\secondExperiments\train_COVID_result.json'
        with open(result_path1, 'w') as fw:
            json.dump(resultDict, fw)