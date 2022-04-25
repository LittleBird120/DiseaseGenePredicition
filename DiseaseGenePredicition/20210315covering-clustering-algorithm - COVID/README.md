# covering-clustering-algorithm
Python实现的覆盖聚类算法

该版本与20210107版本不同的是该版本获取的种子节点方法不一样
主要是基于模块度函数对所有数据集一次性进行聚类（在聚类前不对数据进行分割和归一化处理）
聚类中心求解：
1、求未学习样本中的重点
2、获取所有数据点度数最大所对应的多个数据点
3、求上述数据点离重心最近的点作为聚类中心

聚类半径求解：
1、求所有中心对应的n阶邻居节点至中心的距离集合D={d1,d2,d3,...,dm}，n<=3,dm为某阶邻居节点至聚类中心的欧氏距离
2、以分位数对应的数据点离中心的距离为半径
3、其中分位数以最大模块度Q值以及模块密度的变化确定的，同时Q值只取当次迭代对应的聚类
只考虑模块度函数会存在分辨率限制问题，即：
以模块度最大化为目标，可能无法发现一些规模较小的社团，也就是说当最大模块度值对应的社团结构中包含小于一定规模的社团时，就不能确定这些社团是单独的社团或更小社团的弱连接合并。
4、模块度函数的理解链接：https://blog.csdn.net/marywbrown/article/details/62059231

目录：
resultBeforePolymerization.json是聚合前获得的聚类结果
result.json是聚合后获得的聚类结果
raw_minmax.out是所有归一化后的数据
dataTrain.py中Q值是获取每次迭代时所有聚类的结果
dataTrainEveryQ.py中Q值是获取每次迭代时当次覆盖的结果: Bij=Aij-ki*kj/2m中i、j只是当次迭代获取的覆盖中的节点
dataset/datasplit/Human_everyPro.xls这个文件与之前版本中dataset/Human_everyPro.xls是一样的，这个版本中dataset/Human_everyPro.xls是为了获取种子节点的邻接矩阵重新获取的