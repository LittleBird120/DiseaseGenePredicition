#给定两个基因，如果它们存在于Ｍ个相同的蛋白质复合物中，则共有的M数就是这两个基因之间的相似度
import argparse
import os
import time
import networkx as nx

def parse_args():
	'''
	Parses the node2vec arguments.
	'''
	parser = argparse.ArgumentParser(description="Run")

	parser.add_argument('--input', nargs='?', default='../dataset/uploads/karate.edgelist',
	                    help='Input graph path')

	parser.add_argument('--weighted', dest='weighted', action='store_true',
	                    help='Boolean specifying (un)weighted. Default is unweighted.')
	parser.add_argument('--unweighted', dest='unweighted', action='store_false')
	parser.set_defaults(weighted=True)

	parser.add_argument('--directed', dest='directed', action='store_true',
	                    help='Graph is (un)directed. Default is undirected.')
	parser.add_argument('--undirected', dest='undirected', action='store_false')
	parser.set_defaults(directed=False)

	return parser.parse_args()

def read_graph():
	'''
	Reads the input network in networkx.
	'''
	if args.weighted:
		G = nx.read_edgelist(args.input, nodetype=int, data=(('weight',float),), create_using=nx.DiGraph())
	else:
		G = nx.read_edgelist(args.input, nodetype=int, create_using=nx.DiGraph())
		for edge in G.edges():
			G[edge[0]][edge[1]]['weight'] = 1

	if not args.directed:
		G = G.to_undirected()

	return G

#获取所有复合物的对应的数字标号
def getComplexNum(path,name,file,G):
    filename = path + "/dataset/temp/ad_edge" + name + ".txt"
    nodes_dict = {}
    densityAll = []
    with open(filename, "r") as fr:
        lines_ad_edge = fr.readlines()
        for i in range(len(lines_ad_edge)):
            nodes_dict[i] = lines_ad_edge[i].strip("\n")

    with open(file, "r") as f:
        lines = f.readlines()
        for complex in lines:
            complexList = []
            for node in complex.split("\t"):
                complexList.append(list(nodes_dict.keys())[list(nodes_dict.values()).index(node.strip("\n"))])
            density = one_complex_density(complexList,G,nodes_dict)
            densityAll.append(density)
    return densityAll,lines

#计算单个复合物的密度
def one_complex_density(complex,G,nodes_dict):
    edgesList = G.edges
    edgenum = 0
    length = len(complex)
    # print(length)
    for i in range(len(complex)):
        for j in range(len(complex)):
            if i >= j:
                continue
            elif (complex[i],complex[j]) in edgesList or (complex[j],complex[i]) in edgesList:
                edgenum += 1

    density = (2*edgenum)/(length*(length-1))
    return density

#计算候选基因与致病基因之间的相似度计算
def sim(filePathogenic,fileCandidate,densityAll,lines):
    candidateDict = {}
    with open(filePathogenic, 'r') as f1:
        pathogenic = f1.readlines()

    with open(fileCandidate, 'r') as f2:
        candidate = f2.readlines()

    for i in candidate:
        simCalcute = 0
        every_candidate = i.split("\t")[0]
        for j in pathogenic:
            every_pathogenic = j.split("\t")[0]
            for z in range(len(lines)):
                lineList = lines[z].split("\t")
                if every_pathogenic in lineList and every_candidate in lineList:
                    simCalcute += densityAll[z]
        print("每个候选基因：" + i + "的相似度：")
        print(simCalcute)
        candidateDict[every_candidate] = simCalcute
    return candidateDict

#存储相似度计算
def saveComplexSim(candidateSim):
    fileSim = "../dataset/temp/Candidate_complexSim.txt"
    with open(fileSim,"w") as fw:
        for key,value in candidateSim.items():
            fw.write(key + "\t" + str(value) + "\n")
    fw.close()

if __name__ == '__main__':
    args = parse_args()
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    name = "202008192101"
    fileComplex = path + "/dataset/temp/mls" + name + ".txt"
    filePathogenic = path + "/dataset/uploads/pathogenic_genes.txt"
    fileCandidate = path + "/dataset/uploads/node_degree" + name + ".txt"

    startGraphTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("开始构图：" + startGraphTime)
    G = read_graph()

    startDensityTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("开始计算复合物的密度：" + startDensityTime)
    densityAll,lines = getComplexNum(path,name,fileComplex,G)

    simTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("开始计算相似度：" + simTime)
    candidateSim = sim(filePathogenic,fileCandidate,densityAll,lines)
    saveComplexSim(candidateSim)

    endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("算法结束时间：" + endTime)