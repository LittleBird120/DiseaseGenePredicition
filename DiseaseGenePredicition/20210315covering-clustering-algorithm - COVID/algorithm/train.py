import sys
import os.path
import networkx as nx
from sklearn.model_selection import KFold
from sklearn import preprocessing
import numpy as np
import pandas as pd
np.set_printoptions(suppress=True)
import json
from dataTrainGOCover import DataTrain
from sklearn.model_selection import train_test_split
from time import *

def split(data,ratio_train):
    train,val = train_test_split(data,test_size=1-ratio_train)
    return train,val

#step[1]  加载训练集和验证集
ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
parent_path  = os.path.dirname(ROOT_DIR)
raw_dataset_path = os.path.join(parent_path,r'minmax_out\secondExperiments\seed_minmax.out')#蛋白质互作网络中所有的种子节点的归一化向量
every_pro_path = os.path.join(parent_path,r'dataset\secondExperiments\COVID_Node2Vec.csv')
simGO_path = os.path.join(parent_path,r'dataset\secondExperiments\train_COVID_AllHuman_GoSim.xls')

#网络图的构建
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

#step[2] 划分训练集和验证集，模型训练
lter = 0
train_process = DataTrain(lter, raw_dataset_path, G)#获取核心
train_process.start_train()#保存核心