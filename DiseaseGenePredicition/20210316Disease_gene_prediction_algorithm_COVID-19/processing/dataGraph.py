import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy.interpolate import make_interp_spline
from sklearn import metrics
from sklearn.metrics import auc

mpl.rcParams['font.sans-serif']=['SimHei'] #用来指定默认字体 SimHei为黑体
mpl.rcParams['axes.unicode_minus']=False
x1_data = np.array([0.0, 0.016, 0.034, 0.04, 0.08, 0.22, 0.38, 0.5032, 0.6014, 0.8995, 1.0])  #假阳性率
y1_data = np.array([0.0, 0.1, 0.4660, 0.544, 0.73, 0.78, 0.8, 0.8, 0.8, 1.0, 1.0])
x1_smooth = np.linspace(x1_data.min(), x1_data.max(), 50)
y1_smooth = make_interp_spline(x1_data, y1_data)(x1_smooth)

x2_data = np.array([0.0, 0.02, 0.0319, 0.038, 0.076, 0.26, 0.33, 0.421, 0.6014, 0.8995, 1.0])  #假阳性率
y2_data = np.array([0.0, 0.1, 0.4860, 0.6, 0.72, 0.8, 0.8, 0.8, 0.8, 1.0, 1.0])
x2_smooth = np.linspace(x2_data.min(), x2_data.max(), 50)
y2_smooth = make_interp_spline(x2_data, y2_data)(x2_smooth)

x3_data = np.array([0.0017, 0.0161, 0.0205, 0.0302, 0.0507, 0.31, 0.4643, 0.5032, 0.6014, 0.8995, 1.0])  #假阳性率
y3_data = np.array([0.0, 0.1429, 0.4429, 0.529, 0.6375, 0.8286, 0.861, 0.862, 0.861, 1.0, 1.0])
x3_smooth = np.linspace(x3_data.min(), x3_data.max(), 50)
y3_smooth = make_interp_spline(x3_data, y3_data)(x3_smooth)

x4_data = np.array([0.0, 0.016, 0.034, 0.04, 0.08, 0.22, 0.38, 0.5032, 0.6014, 0.8995, 1.0])  #假阳性率
y4_data = np.array([0.0, 0.1, 0.4660, 0.544, 0.73, 0.78, 0.8, 0.8, 0.8, 1.0, 1.0])
x4_smooth = np.linspace(x4_data.min(), x4_data.max(), 50)
y4_smooth = make_interp_spline(x4_data, y4_data)(x4_smooth)

x5_data = np.array([0.0, 0.014, 0.0219, 0.035, 0.082, 0.19, 0.36, 0.4531, 0.5612, 0.881, 1.0])  #假阳性率
y5_data = np.array([0.0, 0.08, 0.4317, 0.5889, 0.67, 0.78, 0.77, 0.83, 0.80, 0.98, 1.0])
x5_smooth = np.linspace(x5_data.min(), x5_data.max(), 50)
y5_smooth = make_interp_spline(x5_data, y5_data)(x5_smooth)

x6_data = np.array([0.0, 0.014, 0.0198, 0.0236, 0.05763, 0.3054, 0.3819, 0.4669, 0.6014, 0.88, 1.0])  #假阳性率
y6_data = np.array([0.0, 0.092, 0.3756, 0.4912, 0.6719, 0.792, 0.7966, 0.801, 0.8214, 0.9711, 1.0])
x6_smooth = np.linspace(x6_data.min(), x6_data.max(), 50)
y6_smooth = make_interp_spline(x6_data, y6_data)(x6_smooth)

x7_data = np.array([0.0, 0.016, 0.034, 0.04, 0.08, 0.22, 0.38, 0.5032, 0.6014, 0.8995, 1.0])  #假阳性率
y7_data = np.array([0.0, 0.1, 0.4660, 0.544, 0.73, 0.78, 0.8, 0.8, 0.8, 1.0, 1.0])
x7_smooth = np.linspace(x7_data.min(), x7_data.max(), 50)
y7_smooth = make_interp_spline(x7_data, y7_data)(x7_smooth)

x8_data = np.array([0.0, 0.02, 0.0319, 0.038, 0.076, 0.26, 0.33, 0.421, 0.6014, 0.8995, 1.0])  #假阳性率
y8_data = np.array([0.0, 0.1, 0.4860, 0.6, 0.72, 0.8048, 0.8142, 0.8096, 0.8, 0.96, 1.0])
x8_smooth = np.linspace(x8_data.min(), x8_data.max(), 50)
y8_smooth = make_interp_spline(x8_data, y8_data)(x8_smooth)

x9_data = np.array([0.0, 0.0182, 0.0269, 0.0368, 0.0654, 0.31, 0.4005, 0.5032, 0.6014, 0.8995, 1.0])  #假阳性率
y9_data = np.array([0.0, 0.1, 0.4460, 0.53, 0.72, 0.8074, 0.8123, 0.81, 0.82, 1.0, 1.0])
x9_smooth = np.linspace(x9_data.min(), x9_data.max(), 50)
y9_smooth = make_interp_spline(x9_data, y9_data)(x9_smooth)

x10_data = np.array([0.0, 0.025, 0.0269, 0.0368, 0.0614, 0.29, 0.4643, 0.5032, 0.7328, 0.8319, 0.9383])  #假阳性率
y10_data = np.array([0.0, 0.2, 0.4821, 0.5179, 0.7238, 0.83, 0.82, 0.836, 0.827, 1.0, 1.0])
x10_smooth = np.linspace(x10_data.min(), x10_data.max(), 50)
y10_smooth = make_interp_spline(x10_data, y10_data)(x10_smooth)

plt.title('多组对照实验不同参数k的影响')
plt.plot(x1_smooth,y1_smooth, color='black', label='第一组')
plt.plot(x2_smooth,y2_smooth, color='lightcoral', label='第二组')
plt.plot(x3_smooth,y3_smooth, color='sandybrown', label='第三组')
plt.plot(x4_smooth,y4_smooth, color='orange', label='第四组')
plt.plot(x5_smooth,y5_smooth, color='red', label='第五组')
plt.plot(x6_smooth,y6_smooth, color='c', label='第六组')
plt.plot(x7_smooth,y7_smooth, color='skyblue', label='第七组')
plt.plot(x8_smooth,y8_smooth, color='yellowgreen', label='第八组')
plt.plot(x9_smooth,y9_smooth, color='plum', label='第九组')
plt.plot(x10_smooth,y10_smooth, color='pink', label='第十组')
plt.legend()  # 显示图例
plt.xlabel('假阳性率')
plt.ylabel('真阳性率')
plt.show()



#计算AUC值
#第一组
aucs1 = []
aucs1.append(auc(x1_data, y1_data))
auc1 = np.average(aucs1)

#第二组
aucs2 = []
aucs2.append(auc(x2_data, y2_data))
auc2 = np.average(aucs2)

#第三组
aucs3 = []
aucs3.append(auc(x3_data, y3_data))
auc3 = np.average(aucs3)
print(np.average(aucs3))

#第四组
aucs4 = []
aucs4.append(auc(x4_data, y4_data))
auc4 = np.average(aucs4)

#第五组
aucs5 = []
aucs5.append(auc(x5_data, y5_data))
auc5 = np.average(aucs5)

#第六组
aucs6 = []
aucs6.append(auc(x6_data, y6_data))
auc6 = np.average(aucs6)
print(np.average(aucs6))

#第七组
aucs7 = []
aucs7.append(auc(x7_data, y7_data))
auc7 = np.average(aucs7)

#第八组
aucs8 = []
aucs8.append(auc(x8_data, y8_data))
auc8 = np.average(aucs8)

#第九组
aucs9 = []
aucs9.append(auc(x9_data, y9_data))
auc9 = np.average(aucs9)
print(np.average(aucs9))

#第十组
aucs10 = []
aucs10.append(auc(x10_data, y10_data))
auc10 = np.average(aucs10)


y = np.array([auc1, auc2, auc3, auc4, auc5, auc6, auc7, auc8, auc9, auc10])
x = np.array(["第一组","第二组","第三组","第四组","第五组","第六组","第七组","第八组","第九组","第十组"])
plt.title('多组对照实验AUC值')
plt.bar(x, y, width=0.5)
# plt.legend()  # 显示图例
plt.ylabel('AUC')
plt.show()

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']='SimHei'#设置中文显示
plt.figure(figsize=(6,6))#将画布设定为正方形，则绘制的饼图是正圆
label=["E","M","N","S","Nsps"]#定义饼图的标签，标签是列表
explode=[0.01,0.01,0.01,0.01,0.01]#设定各项距离圆心n个半径
#plt.pie(values[-1,3:6],explode=explode,labels=label,autopct='%1.1f%%')#绘制饼图
values=[6, 30, 15, 2, 279]
plt.pie(values,explode=explode,labels=label,autopct='%1.1f%%')#绘制饼图
plt.show()

# encoding=utf-8
from matplotlib import pyplot
import matplotlib.pyplot as plt

x = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
y_train = [0.2413,0.3467,0.3533,0.3629,0.3853,0.3850,0.3936,0.3997,0.3899,0.3985,0.3809]
y_test = [0.3664,0.3679,0.3750,0.4756,0.4967,0.5430,0.5907,0.6613,0.6936,0.5987,0.5763]
# plt.plot(x, y, 'ro-')
# plt.plot(x, y1, 'bo-')
# pl.xlim(-1, 11)  # 限定横轴的范围
# pl.ylim(-1, 110)  # 限定纵轴的范围


plt.plot(x, y_train, marker='o', mec='r', mfc='w', label='DIP Human+CORUM')
plt.plot(x, y_test, marker='*', ms=10, label='DIP Yeast+CYC2008')
plt.legend()  # 让图例生效
plt.xticks(x)

# plt.margins(0)
# plt.subplots_adjust(bottom=0.10)
plt.xlabel('参数t')  # X轴标签
plt.ylabel("F-measure")  # Y轴标签
# pyplot.yticks([0.750, 0.800, 0.850])
# plt.title("A simple plot") #标题
# plt.savefig('D:\\f1.jpg', dpi=900)
plt.show()