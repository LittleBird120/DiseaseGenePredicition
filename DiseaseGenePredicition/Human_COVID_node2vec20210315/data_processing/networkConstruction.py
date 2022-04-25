import json
import os
import pandas as pd
import numpy as np

#获取每个宿主蛋白的相互作用的人类蛋白（其中宿主蛋白是病毒蛋白作用的人类蛋白）
def getAllInteraction(parent_path):
    #获取所有相互作用
    humanInteraction_path = os.path.join(parent_path, r'data\PPIAnalysisData\HIPPIE_database.xls')
    interaction = pd.read_excel(humanInteraction_path)
    interactionDict = {}  #存储所有的人类蛋白相互作用
    for index in interaction.index:
        everyInter = interaction.loc[index].values[0].split()
        interactionDict[index] = [everyInter[0],everyInter[2]]

    #获取宿主蛋白
    hostProtein_path = os.path.join(parent_path, r'data\PPIAnalysisData\viralProtein_humanProtein.csv')
    pro_file = pd.read_csv(hostProtein_path)
    uniprotID = np.array(pro_file["uniprotProteinID"])
    hostArr = []
    for index in range(len(uniprotID)):
        protein = uniprotID[index]
        for k,v in interactionDict.items():
            if protein in v:
                hostArr.extend(v)
        hostArr = list(set(hostArr))

    # 将蛋白的名称转为EntryID
    uniprotHuman_path = os.path.join(parent_path, r'data\PPIAnalysisData\uniprotHuman.xlsx')
    uniprot_df = pd.read_excel(uniprotHuman_path)
    entry = np.array(uniprot_df["Entry"])
    entryName = (np.array(uniprot_df["Entry name"])).tolist()

    hostDict = {}
    noEntryIdHost = []
    for pro in hostArr:
        if pro in entryName:
            entryIndex = entryName.index(pro)
            hostDict[pro] = entry[entryIndex]
        else:
            noEntryIdHost.append(pro)
            continue

    hostList = [i for i in hostArr if i not in noEntryIdHost]
    hostInteraction = []
    for i in range(len(hostList)):
        for j in range(i+1, len(hostList)):
            if [hostList[i], hostList[j]] in interactionDict.values() or [hostList[j],hostList[i]] in interactionDict.values():
                if [hostDict[hostList[i]], hostDict[hostList[j]]] not in hostInteraction and [hostDict[hostList[j]], hostDict[hostList[i]]] not in hostInteraction:
                    hostInteraction.append([hostDict[hostList[i]], hostDict[hostList[j]]])
    allhost = []
    for value in hostInteraction:
        allhost.extend(value)
    allhost = list(set(allhost))
    allhostDict = {}
    for z in allhost:
        allhostDict[list(hostDict.keys())[list(hostDict.values()).index(z)]] = z

    result_host_path = parent_path + r'\data\uploads\host.json'
    with open(result_host_path, 'w') as fw:
        json.dump(allhostDict, fw)

    result_nohost_path = parent_path + r'\data\uploads\noEntryIdHost.json'
    with open(result_nohost_path, 'w') as fw:
        json.dump(noEntryIdHost, fw)

    result_virus_host_path = parent_path + r'\data\uploads\virus_host.json'
    with open(result_virus_host_path, 'w') as fw:
        json.dump(hostInteraction, fw)

#整理完host.json数据后，在该数据的基础上存储这个数据中存在的宿主蛋白
def saveHaveEntryIDHost(parent_path):
    host_filename = os.path.join(parent_path, r'data\uploads\host.json')
    with open(host_filename, 'r') as node_fr:
        nodeslines = node_fr.readlines()
        hostList = json.loads(nodeslines[0])

    hostProtein_path = os.path.join(parent_path, r'data\PPIAnalysisData\viralProtein_humanProtein.csv')
    pro_file = pd.read_csv(hostProtein_path)
    uniprotID = np.array(pro_file["uniprotProteinID"])

    allhost = []
    for index in range(len(uniprotID)):
        protein = uniprotID[index]
        if protein in hostList.keys():
            allhost.append([protein, hostList[protein]])

    result_host_path = parent_path + r'\data\uploads\PartialHost.json'
    with open(result_host_path, 'w') as fw:
        json.dump(allhost, fw)


if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    getAllInteraction(parent_path)
    saveHaveEntryIDHost(parent_path)