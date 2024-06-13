<!--
 * @Descripttion: README.md 
 * @version: 1.0
 * @Author: luxin
 * @Date: 2024-06-10 23:10:25
 * @LastEditTime: 2024-06-13 18:39:46
-->
# D:\Github\Hamamatsu SLM-DGI-supporting-code

 Hamamatsu SLM-DGI-supporting-code

'''
test1.py

1. 直接载入无衍射光场-Mathiue&Gauss光场的bmp相位图 - def loadBmpArray(filepath, x, y, outArray)
2. 生成无衍射光场-Mathiue&Gauss光场的bmp相位图(计算CGH图) - def loadBmpArray(filepath, x, y, outArray)

test2.py

1-修改逻辑,不在函数内部进行图像的反转操作,外部将bmp提前处理成flatten的结构
2-将bmp预处理成flatten存储在arr中,DGI算法单独提供接口, 对应的存储方式都需要改变(存储图片的命名)

test3.py

1. 整理创建图像数据,调制好无衍射光场.bmp-1500张光场图案
2. 测试单张图像的投影I - 用给的接口不需要自己flatten处理
3. 测试单张图像的投影II - 用自己的接口提前进行图像的flatten处理
4. 测试多张图像的投影 - 用自己的函数提前进行图像的flatten处理
5. 测试多设备协同计算关联成像
'''
