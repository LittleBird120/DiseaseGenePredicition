from igraph import Graph, load
import pandas as pd
import numpy as np

def read_file(simGO_path):
    edges_df = pd.read_excel(simGO_path)
    source = np.array(edges_df["protein"])
    target = np.array(edges_df["neghbor_protein"])
    sim = np.array(edges_df["sim"])
    sourceList = []
    targetList = []
    weightList = []

    for i in range(len(source)):
        sourceList.append(source[i].split("_")[0])
        targetList.append(target[i].split("_")[0])
        weightList.append(str(sim[i]))

    write_List(sourceList,targetList,weightList)

def write_List(source,target,weightList):
    filename = "../data/crossValidation/secondExperiments/train_COVID_AllHuman.txt"
    with open(filename,"w") as fw:
        for i in range(len(source)):
            fw.write(source[i] + " " + target[i] + " " + weightList[i] + "\n")

if __name__ == "__main__":
    file = "../data/crossValidation/secondExperiments/train_COVID_AllHuman_GoSim.xls"
    read_file(file)