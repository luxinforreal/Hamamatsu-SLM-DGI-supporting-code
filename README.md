<!--
 * @Descripttion: README.md 
 * @version: 2.0
 * @Author: luxin
 * @Date: 2024-06-10 23:10:25
 * @LastEditTime: 2024-06-16 21:12:38
-->
# D:\Github\Hamamatsu SLM-DGI-supporting-code

 Hamamatsu SLM-DGI-supporting-code

## Test

1.2024/06/13 - test1.py - 测试原来的基本功能是否可以实现

1. 直接载入无衍射光场-Mathiue&Gauss光场的bmp相位图 - def loadBmpArray(filepath, x, y, outArray)
2. 生成无衍射光场-Mathiue&Gauss光场的bmp相位图(计算CGH图) - def loadBmpArray(filepath, x, y, outArray)

2.2024/06/14 - test2.py - 测试自己的代码是否可以显示一张自己图片到屏幕上面(5°)

1. 修改逻辑,不在函数内部进行图像的反转操作,外部将bmp提前处理成flatten的结构
2. 将bmp预处理成flatten存储在arr中,DGI算法单独提供接口, 对应的存储方式都需要改变(存储图片的命名)

3.2024/06/14 - test3.py

1. 整理创建图像数据,调制好无衍射光场.bmp-1500张光场图案
2. 测试单张图像的投影I - 用给的接口不需要自己flatten处理
3. 测试单张图像的投影II - 用自己的接口提前进行图像的flatten处理
4. 测试多张图像的投影 - 用自己的函数提前进行图像的flatten处理
5. 测试多设备协同计算关联成像

4.2024/06/16 20:51:00 test content  

1. 测试是否可以生成，对应的npy文件进行投影；
2. 测试成功，则队Mathiue光场的文件使用makeBmpArray进行.npy文件的生成  

5.2024/06/16 21:51:00 test content  

1. 测试帧率改变的光场投影，对应的npy文件进行投影；
2. 测试成功，则进行简易光场的搭建，先在空气中进行关联成像的测试  
代码中集成daq的控制代码，具体参考main.py()中取巧的同步方式(实际上没有严格的同步机制)，并保存每次的试验结果到所给的路径中，**此时由于没有除了目标之外的变量，每次存储只需要改变路径保存文件名即可**

3.2024/06/17 20:51:00 test content

1. 搭建水下计算关联成像的设备环境，测试水下的计算关联成像；
2. 测试成功则快速进行水下的试验，能做的目标全部处理完成；
最后整理数据，代码上传到Github上面

## Hints

showOn2ndDisplay()函数中的
```Window_Array_to_Display(array, x, y, windowNo, x*y)```
中array传入的必须是C数组类型，也就是得有一个传入的类型必须是指针，通过代码上文中的```Window_Array_to_Display.argtypes = [c_void_p, c_int, c_int, c_int, c_int]```同样有定义c_void_p指的就是一个ctypes中的指针类型，应对后面函数不同的调用方式，有几种不同的解决方式

1.在函数processMultipleImages中，如果调用计算的CGH的代码是：

```java
.....
    outArray = (c_ubyte * (imageWidth * imageHeight))()
    print(f"Processing {filepath}...")
    cgh_array = makeBmpArray(filepath, x, y, outArray)
            
    # 存储生成的CGH图像
    results.append(cgh_array)
```

那么对应的Windows_Array_to_Display()的内部表达式是：

```java
    Window_Array_to_Display(array.ctypes.data_as(ctypes.c_void_p), x, y, windowNo, x*y)
```

2.在函数processMultipleImages中，如果调用计算的CGH的代码是：

```java
.....
    outArray = (c_ubyte * (imageWidth * imageHeight))()
    print(f"Processing {filepath}...")
    cgh_array = makeBmpArray(filepath, x, y, outArray)
            
    # 存储生成的CGH图像
    results.append(outArray)
```

那么对应的Windows_Array_to_Display()的内部表达式是：

```java
    Window_Array_to_Display(ctypes.cast(array, ctypes.POINTER(ctypes.c_ubyte)), x, y, windowNo, x*y)
```
