<!--
 * @Descripttion: README.md 
 * @version: 2.0
 * @Author: luxin
 * @Date: 2024-06-10 23:10:25
 * @LastEditTime: 2024-06-14 16:01:21
-->
# D:\Github\Hamamatsu SLM-DGI-supporting-code

 Hamamatsu SLM-DGI-supporting-code

'''
test1.py - 测试原来的基本功能是否可以实现

1. 直接载入无衍射光场-Mathiue&Gauss光场的bmp相位图 - def loadBmpArray(filepath, x, y, outArray)
2. 生成无衍射光场-Mathiue&Gauss光场的bmp相位图(计算CGH图) - def loadBmpArray(filepath, x, y, outArray)

test2.py - 测试自己的代码是否可以显示一张自己图片到屏幕上面(5°)

1-修改逻辑,不在函数内部进行图像的反转操作,外部将bmp提前处理成flatten的结构
2-将bmp预处理成flatten存储在arr中,DGI算法单独提供接口, 对应的存储方式都需要改变(存储图片的命名)

test3.py

1. 整理创建图像数据,调制好无衍射光场.bmp-1500张光场图案
2. 测试单张图像的投影I - 用给的接口不需要自己flatten处理
3. 测试单张图像的投影II - 用自己的接口提前进行图像的flatten处理
4. 测试多张图像的投影 - 用自己的函数提前进行图像的flatten处理
5. 测试多设备协同计算关联成像
'''

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
    Window_Array_to_Display(
        ctypes.cast(array, ctypes.POINTER(ctypes.c_ubyte)),
        x, y, windowNo, x*y)
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
    Window_Array_to_Display(array.ctypes.data_as(ctypes.c_void_p), x, y, windowNo, x*y)
```
