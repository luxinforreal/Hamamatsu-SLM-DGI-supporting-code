'''
Descripttion: your project
version: 1.0
Author: luxin
Date: 2024-06-23 15:43:59
LastEditTime: 2024-06-23 15:52:48
'''
import numpy as np
from scipy.ndimage import zoom

# 加载npy文件
data = np.load('D:/MICPNet/MICPNet/experiment speckle pattern/np_resized_128x80/100_128x80.npy')

# 确保数据形状正确
assert data.shape == (1500, 128, 80), "数据形状不正确，请检查输入文件"

# 初始化新的数组
new_data = np.zeros((1500, 64, 40))

# 遍历每个二维数组进行缩放
for i in range(data.shape[0]):
    new_data[i] = zoom(data[i], (64/128, 40/80))

# 保存新的npy文件
np.save('100_64x40.npy', new_data)
