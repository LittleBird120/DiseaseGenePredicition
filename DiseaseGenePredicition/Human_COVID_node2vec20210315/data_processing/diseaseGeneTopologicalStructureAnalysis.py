import os
import networkx as nx
import openpyxl
import pandas as pd
import numpy as np
import json
import math

#网络构建
def getNetwork(file_edges,file_hostsPro):
    with open(file_edges, 'r') as edge_fr:
        edgeslines = edge_fr.readlines()
        edgesList = json.loads(edgeslines[0])

    with open(file_hostsPro, 'r') as node_fr:
        nodeslines = node_fr.readlines()
        nodesDict = json.loads(nodeslines[0])

    G = nx.Graph()
    for node in nodesDict.keys():
        G.add_node(node)
    for edge in edgesList:
        G.add_edge(edge[0], edge[1])
    print("图形已构成")

    return nodesDict, G

def analysisTuopu(graph):
    file_hosts = "../data/uploads/PartialHost.json"
    with open(file_hosts, 'r') as edge_fr:
        hostslines = edge_fr.readlines()
        hostsList = json.loads(hostslines[0])
    degree_cen = nx.closeness_centrality(graph)  # 度中心性
    for i in range(len(hostsList)):
        print(degree_cen[hostsList[i][1]])
    print(degree_cen)

if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    file_Go = "../data/COVID_HumanOntology.xls"
    file_edges = "../data/uploads/virus_host.json"
    file_hostsPro = "../data/uploads/hostpro.json"

    nodesDict, G = getNetwork(file_edges, file_hostsPro)
    analysisTuopu(G)