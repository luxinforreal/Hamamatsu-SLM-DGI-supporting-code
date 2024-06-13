'''
Descripttion: The Complete Code for SLM_DGI(Contains the testing code)
version: 1.0
Author: luxin
Date: 2024-06-08 20:07:10
LastEditTime: 2024-06-13 20:24:01
'''
from PIL import Image
import numpy as np
from ctypes import *

import os
import cv2
import copy
from natsort import natsorted, ns

import time

'''MakeBmpArray:
    the function for generating cgh image of import image  and load it into farray for showOn2ndDisplay usage
    String filepath: image file path.
    int x: Pixel number of x-dimension
    int y: Pixel number of y-dimension
    8bit unsigned int array outArray: output array
'''
def makeBmpArray(filepath, x, y, outArray):
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

    # # Tilling the image
    inArray = copy.deepcopy(outArray) 
    Image_Tiling = Lcoslib.Image_Tiling 
    Image_Tiling.argtyes = [c_void_p, c_int, c_int, c_int, c_int, c_int, c_void_p, c_void_p] 

    Image_Tiling(byref(inArray), imageWidth, imageHeight, imageHeight * imageWidth, x, y, byref(c_int(x * y)),
                 pointer(outArray)) 

    return 0


'''MakeBmpArrayFromArray:
    the function for generating cgh image of import image  and load it into farray for showOn2ndDisplay usage
    String filepath: image file path.
    int x: Pixel number of x-dimension
    int y: Pixel number of y-dimension
    8bit unsigned int array outArray: output array
'''
def makeBmpArrayFromFlattenedArray(x, y, outArray):
    # #######  processImagesCombined accomplish this parrt  ########
    
    # im = Image.open(filepath)
    # imageWidth, imageHeight = im.size 
    # im_gray = im.convert("L") 

    # print("Imagesize = {} x {}".format(imageWidth, imageHeight)) 
    # for i in range(imageWidth):
    #     for j in range(imageHeight):
    #         outArray[i + imageWidth * j] = im_gray.getpixel((i, j)) 

    imageWidth = 1272
    imageHeight = 1024
    
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

    # # Tilling the image
    inArray = copy.deepcopy(outArray) 
    Image_Tiling = Lcoslib.Image_Tiling 
    Image_Tiling.argtyes = [c_void_p, c_int, c_int, c_int, c_int, c_int, c_void_p, c_void_p] 

    Image_Tiling(byref(inArray), imageWidth, imageHeight, imageHeight * imageWidth, x, y, byref(c_int(x * y)),
                 pointer(outArray)) 

    return 0


'''LoadBmpArray:
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
    Lcoslib = windll.LoadLibrary("D:\\python_project\\Image_Control.dll") 
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


'''LoadBmpArrayFromFlattenedArray:
    the function for loading BMP files (calcluated CGH image by the cusomter) into farray for showOn2ndDisplay usage.
    String filepath: image file path.
    int x: Pixel number of x-dimension
    int y: Pixel number of y-dimension
    8bit unsigned int array outArray: output array
'''
def loadBmpArrayFromFlattenedArray(x, y, outArray):
    # #######  processImagesCombined accomplish this parrt  ########
    # im = Image.open(filepath)
    # imageWidth, imageHeight = im.size 
    # im_gray = im.convert("L")

    # print("Imagesize = {} x {}".format(imageWidth, imageHeight)) 

    # for i in range(imageWidth):
    #     for j in range(imageHeight):
    #         outArray[i + imageWidth * j] = im_gray.getpixel((i, j)) 

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

    imageWidth = 1272
    imageHeight = 1024

    Image_Tiling(byref(inArray), imageWidth, imageHeight, imageHeight * imageWidth, x, y, byref(c_int(x * y)),
                 pointer(outArray)) 

    return 0


'''processImagesCombined:
    Process a list of images in the given directory and return the processed images and their flattened arrays.
    ref_path (str): The path to the directory containing the images.
    num_images (int): The number of images to process.
    Returns:
        tuple: A tuple containing two elements:
            - img_data (list): A list of processed images as NumPy arrays.
            - reduce img_data dealing code
            - arr (list): A list of flattened arrays of the processed images.
'''
def makeBmpArrayFlatten(filepath, outArray):
    im = Image.open(filepath)
    imageWidth, imageHeight = im.size
    im_gray = im.convert("L")

    print("Image size = {} x {}".format(imageWidth, imageHeight))
    for i in range(imageWidth):
        for j in range(imageHeight):
            outArray[i + imageWidth * j] = im_gray.getpixel((i, j))         
def processImagesCombined(ref_path, num_images):
    os.chdir(ref_path)

    filelist = [f for f in os.listdir(ref_path) if f.endswith('.bmp')]
    filelist = natsorted(filelist)

    if len(filelist) < num_images:
        raise ValueError(f"Not enough images in directory. Found {len(filelist)}, required {num_images}.")

    imageWidth = 1272
    imageHeight = 1024
    
    arr = []
    for i in range(num_images):
        outArray = np.zeros(imageWidth * imageHeight, dtype=np.uint8)
        try:
            makeBmpArrayFlatten(filelist[i], outArray)
            arr.append(outArray)
        except Exception as e:
            print(f"Error processing image {filelist[i]}: {e}")

    return arr

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


'''ShowOn2ndDisplay:
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
    Window_Term.argtyes = [c_int]
    Window_Term.restype = c_int
    Window_Term(windowNo)
    
    return 0

"""DGI Algorithm
    Generate ghost imaging data and save the results as BMP files.
    Args:
        image_data (list): A list of spatial images.
        bucket (list): A list of bucket values corresponding to each spatial image.
        result_save_path (str): The path to save the generated BMP files.
        target (str): The target identifier for the generated files.
        Light_field (str): The different type of the projection light field.
        num_images (int): The size of the generated ghost imaging data.
"""
def ghost_imaging(image_data, bucket, result_save_path, target, speckle_size, num_images):
    if num_images != len(image_data):
        raise ValueError("Number of images provided does not match specified num_images.")
    
    x = 1272
    y = 1024
    
    ghost = np.zeros((y, x))
    bucket_sum = 0
    sum_field = ghost
    ghost_sum = ghost
    
    for i in range(len(image_data)):
        spatial_img1 = image_data[i]
        spatial_img = spatial_img1.astype('float64')
        sum_field = sum_field + spatial_img
        mean_field = sum_field / (i + 1)
        bucket_sum = bucket_sum + bucket[i]
        mean_bucket = bucket_sum / (i + 1)
        ghost_sum = ghost_sum + ((spatial_img - mean_field) * (bucket[i] - mean_bucket)) 
        ghost_final1 = ghost_sum / (i + 1)
        
        print(i)
                      
        if i % 250 == 0 and i != 0:  
            DGI_temp1 = 255 - ghost_final1
            DGI_temp1 = DGI_temp1 - np.min(DGI_temp1)
            DGI_temp1 = DGI_temp1 * 255 / np.max(np.max(DGI_temp1))
            
            DGI_temp1_numpy = DGI_temp1
            
            DGI_temp1 = Image.fromarray(DGI_temp1.astype('uint8')).convert('L')
            DGI_temp1.save(result_save_path + '%s_TGI_n%d_s%s.bmp' % (target, i, speckle_size))
    
    DGI_temp0 = 255 - ghost_final1
    DGI_temp0 = DGI_temp0 - np.min(DGI_temp0)
    DGI_temp0 = DGI_temp0 * 255 / np.max(np.max(DGI_temp0))
    DGI_temp0 = Image.fromarray(DGI_temp0.astype('uint8')).convert('L')
    DGI_temp0.save(result_save_path + '%s_DGI_n1500_s%s.bmp' % (target, speckle_size))



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
    
    # custom data structure to store image
    SELF_FARRAY = (c_uint8 * array_size) * 1500
    self_farray = SELF_FARRAY(0)
    
    # -------- test1 - test the original basic function  -------
    # Display CGH pattern from image file  dll
    # filepath = "Target image sample\\char_hpk_128x128.bmp"
    # makeBmpArray(filepath, x, y, farray)
    # showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, farray)

    # display image from file with dll
    # filepath = "D:\\python_project\\1024.bmp"
    # loadBmpArray(filepath, x, y, farray)
    # showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, farray)
    
    
    # -------- test2 - test advanced fucntion for single projection - old version-------
    # num_image = 1
    # flatten_bmp = []
    # flatten_bmp = processImagesCombined("number_gradation_256x256.bmp", num_image)    
    # makeBmpArrayFromFlattenedArray(x, y, flatten_bmp[0])
    # loadBmpArrayFromFlattenedArray(x, y, farray)
    
    
    # -------- test2 - test advanced fucntion for single projection - new version-------
    result = processMultipleImages("test/test-folder-1-bmp", x, y)
    showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, result)
    
    
    # -------- test3 - test using for loop & projecting multi-images  -------
    
    
    # -------- test4 - test DGI algorithm with Daq and SLM   -------