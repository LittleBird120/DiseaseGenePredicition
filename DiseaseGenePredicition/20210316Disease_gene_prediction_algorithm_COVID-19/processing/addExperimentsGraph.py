#-*- codeing=utf-8 -*-
#@Time:2022/3/25 15:33
#@Author:夏生荣
#@File:addExperimentsGraph.py
#@software:PyCharm
import matplotlib.pyplot as plt

x = [0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.0]
y_precision = [0.9407,0.9390,0.9350,0.9414,0.9383,0.9272,0.9399,0.9312,0.2312,0.1211]
y_recall = [0.6699,0.6652,0.6581,0.6406,0.6334,0.6119,0.6078,0.6012,0.8901,0.2321]

plt.plot(x, y_precision, marker='o', mec='r', mfc='w', label='准确率')
plt.plot(x, y_recall, marker='*', ms=10, label='召回率')
plt.legend()  # 让图例生效
plt.xticks(x)
plt.xlabel('参数t')  # X轴标签
plt.ylabel("F-measure")  # Y轴标签
plt.show()