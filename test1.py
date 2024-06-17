# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 11:32:46 2022

@author: allen
"""

import os
from natsort import natsorted, ns
import numpy as np
import cv2
from PIL import Image

size = 1500 

#ref_path = "C:/Users/allen/Desktop/intensity patterns/random16"
ref_path = "D:/Speckle pattern/RandomField_1280-800/070"
#ref_path = "C:/Users/allen/Desktop/BesselM0-1J-speckle/BesselM1J-50-s100-5"

##ref_path = "C:/Users/allen/Desktop/intensity patterns/random48"

os.chdir(ref_path)

filelist = [f for f in os.listdir(ref_path) if f.endswith('.png')]
filelist = natsorted(filelist)

img_data = []
for i in range(size):
    img = cv2.imread(filelist[i], cv2.IMREAD_GRAYSCALE)
    img_data.append(img)
img_data = np.asarray(img_data)

arr = []
for k in range(size):
    image = img_data[k].flatten()
    arr.append(image)
arr = np.asarray(arr)


from ALP4 import *
import time
from daqmx import NIDAQmxInstrument, AnalogInput

path = 'D:/Ghost Imaing Program/python/DMD_Control'
os.chdir(path)

# daq = NIDAQmxInstrument()

# Load the Vialux .dll
DMD = ALP4(version = '4.3')
# Initialize the device
DMD.Initialize()

# data = []

# Binary amplitude image (0 or 1)
bitDepth = 1    
imgBlack = np.zeros([DMD.nSizeY, DMD.nSizeX])
# imgWhite = np.ones([DMD.nSizeY,DMD.nSizeX])*(2**8-1)
# imgSeq  = np.concatenate([imgBlack.ravel(),imgWhite.ravel()])
# img_Seq  = np.concatenate([img_data[0].ravel(),img_data[1].ravel(),img_data[2].ravel(),
#                            img_data[3].ravel(),img_data[4].ravel(),img_data[5].ravel(),
#                            img_data[6].ravel(),img_data[7].ravel(),img_data[8].ravel(),
#                            img_data[9].ravel()])

# Allocate the onboard memory for the image sequence (nbImg = number of sequence img)
DMD.SeqAlloc(nbImg = size, bitDepth = bitDepth)
# Send the image sequence as a 1D list/array/numpy array
# DMD.SeqPut(imgData = imgSeq)
DMD.SeqPut(imgData = arr)
# Set image rate to 50 Hz (50 Hz is 50 frame in 1 second)(= 20000 microsecond)
DMD.SetTiming(pictureTime = 50000) 
# 25000 equal to 0.025 second (in 1 second 40 pictures can be printed) X
# 50000 equal to 0.05 second (in 1 second 20 pictures can be printed) X
# 100000 equal to 0.1 second (in 1 second 10 pictures can be printed) X
# 200000 equal to 0.2 second (in 1 second 5 pictures can be printed) O

# Time between the start of two consecutive picture, up to 10^7 microseconds = 10 seconds.
print("start")
# Run the sequence in an infinite loop
DMD.Run()

values = daq.ai0.capture(
    sample_count=1500, rate=20,
    max_voltage=10.0, min_voltage=0,
    # mode='differential', 
    timeout=75.0 #75@1500 100@2000
    )

for i in range(3,0,-1):
    print(f"{i}", end="\r", flush=True)
    time.sleep(1)    # time.sleep(1) means 1 second

DMD.Halt() # Stop the sequence display
DMD.FreeSeq() # Free the sequence from the onboard memory
DMD.Free() # De-allocate the device


import os
import numpy as np
import matplotlib.pyplot as plt
import time
import cv2

data = values
bucket = data
# ghost = np.zeros((800, 1280))
ghost = np.zeros((1024, 1280))
bucket_sum = 0
sum_field = ghost + 0.00001
corr_sum = ghost
number_sum = 0
ghost_sum = ghost
number_sum=0
plt.ion()

for i in range(np.size(data)):

    image = img_data[i]
    img = image.astype('float64')
    sum_field = sum_field+img
    number = np.sum(img)
    number_sum = number + number_sum
    mean_number = number_sum / (i + 1) 
    
        
    print(i)

    # Differential GI
    mean_field = sum_field / (i + 1)
    bucketDebug = bucket[i]
    # bucketDebug = bucketDebug[0]
    bucket_sum = bucket_sum+bucketDebug
    mean_bucket = bucket_sum / (i + 1)
    ghost_sum =ghost_sum + (((img/mean_field) - 1)*(bucketDebug - (mean_bucket*number/mean_number)))
    # isnan = np.isnan(ghost_sum)
    # print(True in isnan)
    
    ghost_final = ghost_sum / (i + 1)

    if i == size:
        break
    if i % 250 == 0 and i != 0:  
            DGI_temp1 = 255 - ghost_final
            DGI_temp1 = DGI_temp1 - np.min(DGI_temp1)
            DGI_temp1 = DGI_temp1 * 255 / np.max(np.max(DGI_temp1))
            
            DGI_temp1_numpy = DGI_temp1
            
            DGI_temp1 = Image.fromarray(DGI_temp1.astype('uint8')).convert('L')
            DGI_temp1.save(result_save_path + '%s_TGI_n%d_s%s.bmp' % (target, i, speckle_size))
DGI_temp0 = 255 - ghost_final
DGI_temp0 = DGI_temp0 - np.min(DGI_temp0)
DGI_temp0 = DGI_temp0 * 255 / np.max(np.max(DGI_temp0))
DGI_temp0 = Image.fromarray(DGI_temp0.astype('uint8')).convert('L')
DGI_temp0.save(result_save_path + '%s_DGI_n1500_s%s.bmp' % (target, speckle_size))


plt.imshow(ghost_final)

from scipy import io
io.savemat('ghost_final.mat',{'data': ghost_final})




import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def compute_ghost_imaging(data, img_data, result_save_path, target, speckle_size):
    """
    Perform Differential Ghost Imaging (DGI) on the provided data and save intermediate and final results.

    Parameters:
    data (ndarray): 1D array of bucket values.
    img_data (ndarray): 3D array of image data with shape (num_images, height, width).
    result_save_path (str): Path where the result images will be saved.
    target (str): Target identifier for the saved files.
    speckle_size (str): Speckle size identifier for the saved files.
    """
    # Initialize parameters and arrays
    ghost = np.zeros((1024, 1280))
    bucket_sum = 0
    sum_field = ghost + 0.00001
    corr_sum = ghost
    number_sum = 0
    ghost_sum = ghost
    number_sum = 0
    plt.ion()

    # Loop through each image and perform DGI calculations
    for i in range(np.size(data)):
        image = img_data[i]
        img = image.astype('float64')
        sum_field += img
        number = np.sum(img)
        number_sum += number
        mean_number = number_sum / (i + 1)
        
        print(i)

        # Differential GI
        mean_field = sum_field / (i + 1)
        bucketDebug = data[i]
        bucket_sum += bucketDebug
        mean_bucket = bucket_sum / (i + 1)
        ghost_sum += ((img / mean_field - 1) * (bucketDebug - (mean_bucket * number / mean_number)))
        ghost_final = ghost_sum / (i + 1)

        if i % 250 == 0 and i != 0:  
            DGI_temp1 = 255 - ghost_final
            DGI_temp1 -= np.min(DGI_temp1)
            DGI_temp1 = DGI_temp1 * 255 / np.max(DGI_temp1)
            DGI_temp1 = Image.fromarray(DGI_temp1.astype('uint8')).convert('L')
            DGI_temp1.save(f"{result_save_path}{target}_TGI_n{i}_s{speckle_size}.bmp")
            DGI_temp1.save(f"")
    # Save the final ghost image
    DGI_temp0 = 255 - ghost_final
    DGI_temp0 -= np.min(DGI_temp0)
    DGI_temp0 = DGI_temp0 * 255 / np.max(DGI_temp0)
    DGI_temp0 = Image.fromarray(DGI_temp0.astype('uint8')).convert('L')
    DGI_temp0.save(f"{result_save_path}{target}_DGI_n{np.size(data)}_s{speckle_size}.bmp")

# Example usage
# compute_ghost_imaging(data, img_data, result_save_path, target, speckle_size)
