'''
Descripttion: your project
version: 1.0
Author: luxin
Date: 2024-06-14 15:35:51
LastEditTime: 2024-06-14 16:27:40
'''
import os
import time
from PIL import Image
import numpy as np
from ctypes import *
import copy
import ctypes
from constants import Constants

def makeBmpArray(filepath, x, y, outArray):
    im = Image.open(filepath)
    imageWidth, imageHeight = im.size 
    im_gray = im.convert("L") 

    print("Imagesize = {} x {}".format(imageWidth, imageHeight)) 
    for i in range(imageWidth):
        for j in range(imageHeight):
            outArray[i + imageWidth * j] = im_gray.getpixel((i, j)) 

    # Lcoslib = windll.LoadLibrary("Image_Control.dll")
    Lcoslib = windll.LoadLibrary(Constants.DLL_PATH) 
    
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
    Lcoslib = windll.LoadLibrary("Constants.DLL_PATH")
    
    # Select LCOS window
    Window_Settings = Lcoslib.Window_Settings
    Window_Settings.argtypes = [c_int, c_int, c_int, c_int]
    Window_Settings.restype = c_int
    Window_Settings(monitorNo, windowNo, xShift, yShift)
    
    # Show pattern
    Window_Array_to_Display = Lcoslib.Window_Array_to_Display
    Window_Array_to_Display.argtypes = [c_void_p, c_int, c_int, c_int, c_int]
    Window_Array_to_Display.restype = c_int
    Window_Array_to_Display(array.ctypes.data_as(ctypes.c_void_p), x, y, windowNo, x*y)
    # Window_Array_to_Display(ctypes.cast(array, ctypes.POINTER(ctypes.c_ubyte)), x, y, windowNo, x*y)
    
    return 0

def processMultipleImages(directory, x, y, npy_stored_path):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith(".bmp"):
            filepath = os.path.join(directory, filename)
            image = Image.open(filepath)
            imageWidth, imageHeight = image.size
            outArray = (c_ubyte * (imageWidth * imageHeight))()
            
            print(f"Processing {filepath}...")
            cgh_array = makeBmpArray(filepath, x, y, outArray)
            
            # save as .npy
            results.append(cgh_array)
            
    results_npy = np.array(results)
    np.save(npy_stored_path, results_npy)
    print(f"CGH images saved to {npy_stored_path}")
        
    return results

def displayCGHImages(results, monitorNo, windowNo, x, xShift, y, yShift, frameRate):
    frameInterval = 1 / frameRate
    Lcoslib = windll.LoadLibrary(Constants.DLL_PATH)

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


def loadCGHImages(npy_stored_path):
    if os.path.exists(npy_stored_path):
        cgh = np.load(npy_stored_path)
        print(f"CGH images loaded from {npy_stored_path}")
        return cgh
    else:
        print(f"File {npy_stored_path} does not exist.")
        return None
        

def display_images_with_frame_rate(images, frame_rate=30):
    num_images = len(images)
    sleep_time = 1 / frame_rate
    
    for i, image_array in enumerate(images):
        print(f"Displaying image {i+1}/{num_images}")
        showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, image_array)
        time.sleep(sleep_time)
        print(i + 1)


if __name__ == "__main__":
    dll_path = Constants.DLL_PATH
    bmp_origin_path = Constants.TEST_BMP_PATH_MULTIPLE
    npy_stored_path = Constants.NPY_STORED_PATH
    x = 1280  
    y = 1024   
    monitorNo = 2 
    windowNo = 0  
    xShift = 0  
    yShift = 0  
    frameRate = 1 
    # results = processMultipleImages(bmp_origin_path, x, y)
    results = loadCGHImages(npy_stored_path)
    if results is None:
        results = processMultipleImages(bmp_origin_path, x, y, npy_stored_path)
    
    try:
        display_images_with_frame_rate(results, frame_rate=1) 
    except KeyboardInterrupt:
        print("Display interrupted by user.")
