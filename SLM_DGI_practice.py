'''
Descripttion: SLM_DGI_Logical.py
version: 1.0
Author: luxin
Date: 2024-06-08 14:32:30
LastEditTime: 2024-06-08 20:35:40
'''
from PIL import Image
import numpy as np
from ctypes import *

import os
import cv2
import copy
from natsort import natsorted, ns

import time

'''
the function for generating cgh image of import image  and load it into farray for showOn2ndDisplay usage
String filepath: image file path.
int x: Pixel number of x-dimension
int y: Pixel number of y-dimension
8bit unsigned int array outArray: output array
'''
def makeBmpArraFromFilepath(filepath, x, y, outArray):
    im = Image.open(filepath)
    imageWidth, imageHeight = im.size 
    im_gray = im.convert("L") 

    print("Imagesize = {} x {}".format(imageWidth, imageHeight)) 

    for i in range(imageWidth):
        for j in range(imageHeight):
            outArray[i + imageWidth * j] = im_gray.getpixel((i, j)) 
    # Lcoslib = cdll.LoadLibrary("Image_Control.dll")
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
    Image_Tiling.restype = c_int

    Image_Tiling(byref(inArray), imageWidth, imageHeight, imageHeight * imageWidth, x, y, byref(c_int(x * y)),
                 pointer(outArray))

    return 0


'''
the function for generating cgh image of import image  and load it into farray for showOn2ndDisplay usage
Array: unflattened 8bit unsigned int array.
int x: Pixel number of x-dimension
int y: Pixel number of y-dimension
8bit unsigned int array outArray: output array
'''
def makeBmpArraFromArray(img_data, x, y, outArray):
    im = Image.open(img_data)
    imageWidth, imageHeight = im.size 
    im_gray = im.convert("L")

    print("Imagesize = {} x {}".format(imageWidth, imageHeight)) 

    for i in range(imageWidth):
        for j in range(imageHeight):
            outArray[i + imageWidth * j] = im_gray.getpixel((i, j)) 
    # Lcoslib = cdll.LoadLibrary("Image_Control.dll")
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
    Image_Tiling.restype = c_int

    Image_Tiling(byref(inArray), imageWidth, imageHeight, imageHeight * imageWidth, x, y, byref(c_int(x * y)),
                 pointer(outArray))

    return 0


'''
the function for loading BMP files (calcluated CGH image by the cusomter) into farray for showOn2ndDisplay usage.
String filepath: image file path.
int x: Pixel number of x-dimension
int y: Pixel number of y-dimension
8bit unsigned int array outArray: output array
'''
def loadBmpArray(filepath, x, y, outArray):
    im = Image.open(filepath)
    imageWidth, imageHeight = im.size 
    im_gray = im.convert("L") 

    print("Imagesize = {} x {}".format(imageWidth, imageHeight)) 

    for i in range(imageWidth):
        for j in range(imageHeight):
            outArray[i + imageWidth * j] = im_gray.getpixel((i, j)) 
    # Lcoslib = cdll.LoadLibrary("Image_Control.dll")
    Lcoslib = windll.LoadLibrary("Image_Control.dll") 
    # #
    # # # Create CGH
    # # inArray = copy.deepcopy(outArray)
    # # Create_CGH_OC = Lcoslib.Create_CGH_OC
    # # Create_CGH_OC.argtyes = [c_void_p, c_int, c_int, c_int, c_int, c_void_p, c_void_p]
    # # Create_CGH_OC.restype = c_int
    # #
    # # repNo = 100
    # # progressBar = 1
    # # Create_CGH_OC(byref(inArray), repNo, progressBar, imageWidth, imageHeight, byref(c_int(imageHeight * imageWidth)),
    # #               byref(outArray))
    #
    # # Tilling the image
    inArray = copy.deepcopy(outArray) 
    Image_Tiling = Lcoslib.Image_Tiling 
    Image_Tiling.argtypes = [c_void_p, c_int, c_int, c_int, c_int, c_int, c_void_p, c_void_p] 
    Image_Tiling.restype = c_int

    Image_Tiling(byref(inArray), imageWidth, imageHeight, imageHeight * imageWidth, x, y, byref(c_int(x * y)),
                 pointer(outArray))

    return 0


'''
the function for showing on LCOS display
int monitorNo: 
int windowNo:
int x: Pixel number of x-dimension
int xShift: shift pixels of x-dimension
int y: Pixel number of y-dimension
int yShift: shift pixels of y-dimension
8bit unsigned int array array: output array
'''
def showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, array):
    Lcoslib = windll.LoadLibrary("Image_Control.dll")
    
    #Select LCOS window
    Window_Settings = Lcoslib.Window_Settings
    Window_Settings.argtypes = [c_int, c_int, c_int, c_int]
    Window_Settings.restype = c_int
    Window_Settings(monitorNo, windowNo, xShift, yShift)
    
    #Show pattern
    Window_Array_to_Display = Lcoslib.Window_Array_to_Display
    Window_Array_to_Display.argtypes = [c_void_p, c_int, c_int, c_int, c_int]
    Window_Array_to_Display.restype = c_int
    Window_Array_to_Display(array, x, y, windowNo, x*y)
    
    #wait until enter key input
    input("please input enter key...")
    
    #close the window
    Window_Term = Lcoslib.Window_Term
    Window_Term.argtypes = [c_int]
    Window_Term.restype = c_int
    Window_Term(windowNo)
    
    return 0


def main():

    # pixelpitch(0: 20um 1: 12.5um)
    pitch = 1
    
    # LCOS pixel resolution
    x = 1272
    y = 1024
    
    # LCOS-SML monitor number setting 
    monitorNo = 2
    windowNo = 0
    xShift = 0
    yShift = 0
    
    # pixel number 总共像素的个数，方便后面函数调用
    array_size = x * y

    # make the 8bit unsigned integer array type 初始化用于存储相位图,结果是_ctypes.PyCArrayType
    FARRAY = c_uint8 * array_size

    # make the 8bit unsigned integer array instance
    # initialize the array - element 0
    farray = FARRAY(0) 
    farray2 = FARRAY(0)
    farray3 = FARRAY(0)
    
    # 自定义数据结构存储图像
    SELF_FARRAY = (c_uint8 * array_size) * 1500
    self_farray = SELF_FARRAY(0)
    
    
    # Display CGH pattern array with using dll 生成自定义路径文件的相位图
    # 最好把数据处理单独出来， DGI的算法同样单独出来写成函数结构，具体变量都按照模板进行划分
    num_images = 1500
    ref_path = "D:/Speckle pattern/RandomField_1280-800/070"
    os.chdir(ref_path)

    filelist = [f for f in os.listdir(ref_path) if f.endswith('.bmp')]
    filelist = natsorted(filelist)

    # store .bmp image in the 2D img_array
    img_data = []
    for i in range(num_images):
        try:
            img = cv2.imread(filelist[i], cv2.IMREAD_GRAYSCALE)
            if img is None:
                raise ValueError(f"Failed to load image: {filelist[i]}")
            img_data.append(img)
        except Exception as e:
            print(f"Error loading image {filelist[i]}: {e}")

    # stroe .bmp as 1D array
    arr = []
    for k in range(num_images):
        try:
            image = img_data[k].flatten()
            arr.append(image)
        except Exception as e:
            print(f"Error processing image {k}: {e}")

    # Display the images 
    for i in range(num_images):
        print(f"Displaying image {i+1}/{num_images}")
        makeBmpArraFromArray(arr[i], x, y, farray)
        showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, farray)
        
    
    return 0