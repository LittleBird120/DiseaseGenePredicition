#算法性能的比较
import numpy as np
import matplotlib.pyplot as plt

#获取所有候选蛋白和测试集（都是宿主蛋白）
def read_file(file,filePathogenic):
    pathogenic = []
    predictHostProtein = []  #预测的宿主蛋白
    notHostProtein = []    #判定为不是宿主蛋白
    with open(filePathogenic,"r") as fr:
        pathogeniclines = fr.readlines()
        for i in range(len(pathogeniclines)):
            pathogenic.append(pathogeniclines[i].strip("\n"))

    with open(file,"r") as f:
        Candidatelines = f.readlines()
        k = int(len(Candidatelines)*0.7)
        print("获取前"+str(k)+"条数据")
        for j in range(len(Candidatelines)):
            if j <= k:
                CandidateList = Candidatelines[j].strip("\n").split("\t")
                predictHostProtein.append(CandidateList[0])
            else:
                CandidateList = Candidatelines[j].strip("\n").split("\t")
                notHostProtein.append(CandidateList[0])

    return pathogenic,predictHostProtein,notHostProtein

#混淆矩阵计算
def calculationConfusionMatrixElement(pathogenic, predictHostProtein, notHostProtein):
    pro_path = "../dataset/result/prePro.txt"
    TP = 0   #将正类预测为正类数
    TN = 0   #将负类预测为负类数
    FP = 0   #将负类预测为正类数误报
    FN = 0   #将正类预测为负类数漏报
    prePro = []
    for preNode in predictHostProtein:
        if preNode in pathogenic:
            TP += 1
            prePro.append(preNode)
        else:
            FP += 1

    for notNode in notHostProtein:
        if notNode in pathogenic:
            FN += 1
        else:
            TN += 1

    np.savetxt(pro_path, prePro, fmt='%s')
    return TP, TN, FP, FN

def getEvaluating(TP, TN, FP, FN):
    TPR = TP/(TP+FN)
    FPR = FP/(TN+FP)
    print("真阳性率为："+str(format(TPR,".4f"))+"，假阳性率为："+str(format(FPR,".4f")))

if __name__ == '__main__':
    filePathogenic = "../dataset/uploads/secondExperiments/train.txt"   #测试集
    file = "../dataset/result/allSimilarity.txt"
    pathogenic, predictHostProtein, notHostProtein = read_file(file, filePathogenic)
    TP, TN, FP, FN = calculationConfusionMatrixElement(pathogenic, predictHostProtein, notHostProtein)
    getEvaluating(TP, TN, FP, FN)