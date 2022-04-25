#计算总的相似度作为评分
import numpy as np

def read_file(fileComplexSim,fileNodeVecSim):
    with open(fileComplexSim, 'r') as f1:
        ComplexSim = f1.readlines()
        ComplexSimDict = {}
        for i in range(len(ComplexSim)):
            everyComplexSim = ComplexSim[i].strip("\n").split("\t")
            ComplexSimDict[everyComplexSim[0]] = float(everyComplexSim[1])

    with open(fileNodeVecSim, 'r') as f2:
        NodeVecSim = f2.readlines()
        NodeVecSimDict = {}
        for i in range(len(NodeVecSim)):
            everyNodeVecSim = NodeVecSim[i].strip("\n").split("\t")
            NodeVecSimDict[everyNodeVecSim[0]] = float(everyNodeVecSim[1])
    return ComplexSimDict,NodeVecSimDict

#相似度计算
def similarity(ComplexSimDict,NodeVecSimDict):
    simAllDict = {}
    for key,valueComplexSim in ComplexSimDict.items():
        sim = valueComplexSim * NodeVecSimDict[key]
        simAllDict[key] = sim
    simAllDict = sorted(simAllDict.items(), key=lambda item: item[1], reverse=True)
    return simAllDict

def save(simAllDict):
    fileSim = "../dataset/result/similarity.txt"
    with open(fileSim, "w") as fw:
        for j in range(len(simAllDict)):
            fw.write(simAllDict[j][0] + "\t" + str(simAllDict[j][1]) + "\n")
    fw.close()

if __name__ == '__main__':
    fileComplexSim = "../dataset/result/Candidate_complexSim.txt"
    fileNodeVecSim = "../dataset/result/Candidate_NodeVecSim.txt"
    ComplexSimDict, NodeVecSimDict = read_file(fileComplexSim, fileNodeVecSim)
    simAllDict = similarity(ComplexSimDict, NodeVecSimDict)
    save(simAllDict)