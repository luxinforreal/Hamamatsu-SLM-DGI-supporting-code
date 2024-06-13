import os
import time
from PIL import Image
import numpy as np
from ctypes import *
import copy

def makeBmpArray(filepath, x, y, outArray):
    im = Image.open(filepath)
    imageWidth, imageHeight = im.size 
    im_gray = im.convert("L") 

    print("Imagesize = {} x {}".format(imageWidth, imageHeight)) 
    for i in range(imageWidth):
        for j in range(imageHeight):
            outArray[i + imageWidth * j] = im_gray.getpixel((i, j)) 

    # Lcoslib = windll.LoadLibrary("Image_Control.dll")  # 根据你的平台选择正确的LoadLibrary方法
    Lcoslib = windll.LoadLibrary("Image_Control.dll") 
    
    # Create CGH
    inArray = copy.deepcopy(outArray) 
    Create_CGH_OC = Lcoslib.Create_CGH_OC 
    Create_CGH_OC.argtypes = [c_void_p, c_int, c_int, c_int, c_int, c_void_p, c_void_p] 
    Create_CGH_OC.restype = c_int 

    repNo = 100  
    progressBar = 1  
    Create_CGH_OC(byref(inArray), repNo, progressBar, imageWidth, imageHeight, byref(c_int(imageHeight * imageWidth)),
                  byref(outArray))

    # Tilling the image
    inArray = copy.deepcopy(outArray) 
    Image_Tiling = Lcoslib.Image_Tiling 
    Image_Tiling.argtypes = [c_void_p, c_int, c_int, c_int, c_int, c_int, c_void_p, c_void_p] 

    Image_Tiling(byref(inArray), imageWidth, imageHeight, imageHeight * imageWidth, x, y, byref(c_int(x * y)),
                 pointer(outArray)) 

    return np.array(outArray).reshape((imageHeight, imageWidth))

def showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, array):
    Lcoslib = windll.LoadLibrary("Image_Control.dll")
    
    # Select LCOS window
    Window_Settings = Lcoslib.Window_Settings
    Window_Settings.argtypes = [c_int, c_int, c_int, c_int]
    Window_Settings.restype = c_int
    Window_Settings(monitorNo, windowNo, xShift, yShift)
    
    # Show pattern
    Window_Array_to_Display = Lcoslib.Window_Array_to_Display
    Window_Array_to_Display.argtypes = [c_void_p, c_int, c_int, c_int, c_int]
    Window_Array_to_Display.restype = c_int
    Window_Array_to_Display(array, x, y, windowNo, x*y)
    
    return 0

def processMultipleImages(directory, x, y):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith(".bmp"):
            filepath = os.path.join(directory, filename)
            image = Image.open(filepath)
            imageWidth, imageHeight = image.size
            outArray = (c_ubyte * (imageWidth * imageHeight))()
            
            print(f"Processing {filepath}...")
            cgh_array = makeBmpArray(filepath, x, y, outArray)
            
            # 存储生成的CGH图像
            results.append(outArray)
        
    return results

def displayCGHImages(results, monitorNo, windowNo, x, xShift, y, yShift, frameRate):
    frameInterval = 1 / frameRate
    Lcoslib = windll.LoadLibrary("Image_Control.dll")

    for array in results:
        showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, array)
        time.sleep(frameInterval)
    
    # Wait until enter key input to close the window
    input("Please press the enter key to close the window...")

    # Close the window
    Window_Term = Lcoslib.Window_Term
    Window_Term.argtypes = [c_int]
    Window_Term.restype = c_int
    Window_Term(windowNo)

# 示例用法
directory = "path_to_your_bmp_images"  # 替换为你的BMP图像文件夹路径
x = 1280  # 目标X维度像素数
y = 1024   # 目标Y维度像素数
monitorNo = 2  # LCOS显示器编号
windowNo = 0  # 窗口编号
xShift = 0  # X方向偏移量
yShift = 0  # Y方向偏移量
frameRate = 20  # 设定的帧率

# 处理所有图像并生成CGH图像
results = processMultipleImages(directory, x, y)

# 按照帧率显示CGH图像
displayCGHImages(results, monitorNo, windowNo, x, xShift, y, yShift, frameRate)
