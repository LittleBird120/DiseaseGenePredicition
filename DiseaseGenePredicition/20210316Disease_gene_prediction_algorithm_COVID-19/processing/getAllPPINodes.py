#-*- codeing=utf-8 -*-
#@Time:2022/3/25 10:07
#@Author:夏生荣
#@File:getAllPPINodes.py
#@software:PyCharm
import os
import pandas as pd
import numpy as np

#得到病毒蛋白相互作用网络的全部节点
ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
parent_path = os.path.dirname(ROOT_DIR)
every_pro_path = os.path.join(parent_path, r'dataset\temp\secondExperiments\COVID_Node2Vec.csv')
pro_file = pd.read_csv(every_pro_path)
pro = np.array(pro_file["name"])
list = []
for i in range(len(pro)):
    print(pro[i])
    list.append(pro[i])
print(list.__len__())