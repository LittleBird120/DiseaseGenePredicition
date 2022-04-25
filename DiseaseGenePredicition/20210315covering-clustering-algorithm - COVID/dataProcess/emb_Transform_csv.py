import json
import os
import pandas as pd
from collections import OrderedDict

#获取所有节点的向量表示形式
def getNodeVector(parent_path):
    fileEMB = os.path.join(parent_path, r'dataset\secondExperiments\trainNode2Vec.emb')
    nodeVecDict = {}
    with open(fileEMB, "r") as f:
        lines = f.readlines()
        #print(lines)
        for i in range(1,len(lines)):
            every_nodeVecList = []
            node_vector_list = lines[i].strip("\n").split(" ")
            for j in range(1,len(node_vector_list)):
                every_nodeVecList.append(float(node_vector_list[j]))
            nodeVecDict[int(node_vector_list[0])] = every_nodeVecList

    return nodeVecDict

def savetocsv(parent_path,nodeVecDict):
    every_pro_path = os.path.join(parent_path, r'dataset\secondExperiments\train_host.json')
    with open(every_pro_path, 'r') as node_fr:
        nodeslines = node_fr.readlines()
        hostDict = json.loads(nodeslines[0],object_pairs_hook=OrderedDict)
    pro = [node for node,go in hostDict.items()]

    name = ["name","node2vec"]
    allnode = []
    for k,v in nodeVecDict.items():
        nodelist = []
        nodelist.append(pro[k])
        nodelist.append(v)
        allnode.append(nodelist)
    filedata = pd.DataFrame(columns=name,data=allnode)
    filedata.to_csv("../dataset/secondExperiments/COVID_Node2Vec.csv")

if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    nodeVecDict = getNodeVector(parent_path)
    savetocsv(parent_path,nodeVecDict)