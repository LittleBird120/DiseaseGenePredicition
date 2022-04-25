from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import sys
import os.path
import numpy as np
np.set_printoptions(suppress=True)

def train_test_val_split(df,ratio_train,ratio_test,ratio_val):
    train, middle = train_test_split(df,test_size=1-ratio_train)
    ratio=ratio_val/(1-ratio_train)
    test,validation =train_test_split(middle,test_size=ratio)
    return train,test,validation

def split(data,ratio_train):
    train,test = train_test_split(data,test_size=1-ratio_train)
    return train,test

#In[1] 加载路径
ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
parent_path  = os.path.dirname(ROOT_DIR)
raw_dataset_path = os.path.join(parent_path,r'dataset\secondExperiments\protein_matrix.out')
raw_minmax_path = os.path.join(parent_path,r'minmax_out\secondExperiments\raw_minmax.out')
# train_val_minmax_path = os.path.join(parent_path,r'minmax_out\train_val_minmax.out')
# test_minmax_path = os.path.join(parent_path,r'minmax_out\test_minmax.out')
raw_dataset = np.loadtxt(raw_dataset_path, delimiter = ',')

# In[2] 数据集归一化处理
m,n = raw_dataset.shape
# train_val_dataset,test_dataset = split(raw_dataset,0.8)
#
# #In[4] 保存数据
# np.savetxt(train_val_minmax_path, train_val_dataset, delimiter=',', fmt='%s')
# np.savetxt(test_minmax_path, test_dataset, delimiter=',', fmt='%s')

#train_val_dataset,test_dataset = split(raw_dataset,0.8)
min_max_scaler = preprocessing.MinMaxScaler().fit(raw_dataset[..., 0:n-2])

raw_dataset_tag = raw_dataset[..., n-2:n - 1]
rawSize = raw_dataset_tag.size
raw_dataset_tag = raw_dataset_tag.reshape(rawSize, 1)

#获取度的标签
raw_degree_tag = raw_dataset[..., n - 1]
raw_degree_Size = raw_degree_tag.size
raw_degree_tag = raw_degree_tag.reshape(raw_degree_Size, 1)

raw_dataset_minmax = min_max_scaler.transform(raw_dataset[..., 0:n-2])
raw_dataset_minmax = np.concatenate((raw_dataset_minmax, raw_dataset_tag), axis=1)
raw_dataset_minmax = np.concatenate((raw_dataset_minmax, raw_degree_tag), axis=1)

#In[4] 保存数据
np.savetxt(raw_minmax_path, raw_dataset_minmax, delimiter=',', fmt='%s')