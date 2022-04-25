import json
import math
import os

import openpyxl
import pandas as pd
import numpy as np
from xlutils.copy import copy
import xlwt
import xlrd

#获取每个蛋白的功能注释
def readUniprot(parent_path):
    uniprot_filename = os.path.join(parent_path, r'data\PPIAnalysisData\uniprotHuman.xlsx')
    host_filename = os.path.join(parent_path, r'data\uploads\host.json')
    uniprot_df = pd.read_excel(uniprot_filename)
    entry = (np.array(uniprot_df["Entry"])).tolist()
    GOIDs = (np.array(uniprot_df["Gene ontology IDs"])).tolist()

    with open(host_filename, 'r') as node_fr:
        nodeslines = node_fr.readlines()
        nodeList = json.loads(nodeslines[0])

    host_GOIDs = {}
    for node in nodeList.values():
        nodeIndex = entry.index(node)
        proGOIDs = GOIDs[nodeIndex]
        host_GOIDs[node] = proGOIDs

    result_host_path = parent_path + r'\data\uploads\hostpro.json'
    with open(result_host_path, 'w') as fw:
        json.dump(host_GOIDs, fw)

#将人类蛋白质中的功能注释按照三个本体分隔开，便于后期的加权计算
def readnodes_protein(parent_path):
    filename = os.path.join(parent_path, r'data\uploads\hostpro.json')
    filenameAll = os.path.join(parent_path, r'data\Term.info.xls')
    with open(filename, 'r') as node_fr:
        nodeslines = node_fr.readlines()
        nodeList = json.loads(nodeslines[0])
        print(nodeList)

    df_all = pd.read_excel(filenameAll)
    id_all = df_all["id"]
    namespace = df_all["namespace"]

    name = list(nodeList.keys())

    nodes_dict = []
    for node,go in nodeList.items():
        BP = ""
        CC = ""
        MF = ""
        dict = {}
        if type(go) != float and go != 'nan':
            id_list = go.split("; ")
            for j in range(len(id_list)):
                if id_list[j] in id_all.array:
                    if namespace[j] == "biological_process":
                        BP += id_list[j] + "|"
                    elif namespace[j] == "cellular_component":
                        CC += id_list[j] + "|"
                    elif namespace[j] == "molecular_function":
                        MF += id_list[j] + "|"
        else:
            print(type(go), "::::", go)
            print("error")

        dict["BP"] = BP[:-1]
        dict["CC"] = CC[:-1]
        dict["MF"] = MF[:-1]
        nodes_dict.append(dict)
    name = list(nodeList.keys())
    save_to_csv(nodes_dict, name)

def save_to_csv(nodes_dict,name):
    file_path = "../data/COVID_HumanOntology1.xls"
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'BP', cell_overwrite_ok=True)  # 创建sheet
    sheet2 = f.add_sheet(u'MF', cell_overwrite_ok=True)
    sheet3 = f.add_sheet(u'CC', cell_overwrite_ok=True)
    for i in range(len(nodes_dict)):
        BP = nodes_dict[i]["BP"]
        CC = nodes_dict[i]["CC"]
        MF = nodes_dict[i]["MF"]
        sheet1.write(i, 0, name[i])
        if len(BP) == 0:
            sheet1.write(i, 1, "NULL")
        else:
            sheet1.write(i ,1, BP)
        sheet1.write(i, 2, "P")
        sheet2.write(i, 0, name[i])
        if len(MF) == 0:
            sheet2.write(i, 1, "NULL")
        else:
            sheet2.write(i, 1, MF)
        sheet2.write(i, 2, "F")
        sheet3.write(i, 0, name[i])
        if len(CC) == 0:
            sheet3.write(i, 1, "NULL")
        else:
            sheet3.write(i, 1, CC)
        sheet3.write(i, 2, "C")

    f.save(file_path)  # 保存文件

def AllAncestor():
    file2 = "../data/functionalClosure.xls"
    df2 = pd.read_excel(file2)
    id = df2["term"]
    id = np.array(id)
    ancestor = df2["ancestor"]
    ancestor = np.array(ancestor)
    for a in range(3):
        arr = []
        arr.append(["all"])
        file1 = "../data/COVID_HumanOntology.xls"
        df1 = pd.read_excel(file1, sheet_name=a)
        term = df1["term"]
        term = np.array(term)
        for i in term:
            term_list = []
            if i == "Null":
                term_list.append(i)
            else:
                if isinstance(i, float):
                    i_list = list(str(i))
                else:
                    i_list = i.split("|")
                for j in i_list:
                    term_list.append(j)
                    index = np.where(id == j)
                    if len(index[0]) == 0:
                        continue
                    else:
                        row = index[0][0]
                        anc_list = ancestor[row].split("|")
                        for z in anc_list:
                            term_list.append(z)
                term_list = list(set(term_list))
            arr.append(term_list)
        datas = np.array(arr)
        to_excel_all(datas,a,file1)

def to_excel_all(datas,index,file_path):
    rb = xlrd.open_workbook(file_path, formatting_info=True)
    wb = copy(rb)
    ws = wb.get_sheet(index)

    # 将数据写入第 i 行，第 j 列
    i = 0
    for data in datas:
        for j in range(len(data)):
            if len(data) == 1:
                ws.write(i, 5, data[j])
            else:
                if j == 0:
                    str = data[j]
                else:
                    str += "|" + data[j]
                ws.write(i, 5, str)
        i = i + 1

    wb.save(file_path)

if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    file_edges = "../data/uploads/virus_host.json"
    readUniprot(parent_path)
    readnodes_protein(parent_path)
    AllAncestor()