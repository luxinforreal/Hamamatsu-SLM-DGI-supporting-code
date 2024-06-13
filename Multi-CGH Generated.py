import os
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
            results.append(cgh_array)
        
    return results



def main():
    # pixelpitch(0: 20um 1: 12.5um)
    pitch = 1
    
    # LCOS pixel resolution
    x = 1280
    y = 1024
    
    # LCOS-SML monitor number setting 
    monitorNo = 2
    windowNo = 0
    xShift = 0
    yShift = 0
    
    # pixel number - 1272 x 1024
    array_size = x * y

    # make the 8bit unsigned integer array type
    FARRAY = c_uint8 * array_size

    # make the 8bit unsigned integer array instance
    # initialize the array - element 0
    farray = FARRAY(0) 
    
    
    directory = "test/test-folder-1-bmp" 
    x = 1280  
    y = 800  
    results = processMultipleImages(directory, x, y)

    for i, result in enumerate(results):
        print(f"Processed image {i+1}, output array shape: {result.shape}")
    