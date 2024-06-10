# -*- coding: utf-8 -*-
"""
Created on Mon May 18 14:10:00 2020

@author: HPK
"""

from PIL import Image
import numpy as np
from ctypes import *
import copy



    # pixelpitch(0: 20um 1: 12.5um)
pitch = 1

    # LCOS pixel size
x = 1280
y = 1024

    # LCOS-SML monitor number setting
monitorNo = 2
windowNo = 0
xShift = 0
yShift = 0

    # pixel number
array_size = x * y

    # make the 8bit unsigned integer array type
FARRAY = c_uint8 * array_size
print(type(FARRAY))

    # make the 8bit unsigned integer array instance
farray = FARRAY(0)
#print(type(farray))
#farray2 = FARRAY(0)
#farray3 = FARRAY(0)


def showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, array):
    Lcoslib = windll.LoadLibrary("D:\\python_project\\Image_Control.dll")

    # Select LCOS window
    Window_Settings = Lcoslib.Window_Settings
    Window_Settings.argtypes = [c_int, c_int, c_int, c_int]
    Window_Settings.restype = c_int
    Window_Settings(monitorNo, windowNo, xShift, yShift)

    # Show pattern
    Window_Array_to_Display = Lcoslib.Window_Array_to_Display
    Window_Array_to_Display.argtypes = [c_void_p, c_int, c_int, c_int, c_int]
    Window_Array_to_Display.restype = c_int
    Window_Array_to_Display(array, x, y, windowNo, x * y)

    # wait until enter key input
    input("please input enter key...")

    # close the window
    Window_Term = Lcoslib.Window_Term
    Window_Term.argtyes = [c_int]
    Window_Term.restype = c_int
    Window_Term(windowNo)

    return 0
'''
the function for making AxiconLens pattern array
double top: Top level of AxiconLens pattern. (/pi rad)
int pitch: Pixel pitch. 0: 20um 1: 1.25um
int x: Pixel number of x-dimension
int y: Pixel number of y-dimension
8bit unsigned integer array array: output array
'''
def makeAxiconLensArray(top, pitch, x, y, array):
    #Lcoslib = cdll.LoadLibrary("Image_Control.dll") #for cdll
    Lcoslib = windll.LoadLibrary("D:\\python_project\\Image_Control.dll") #for windll
    AxiconLens = Lcoslib.AxiconLens
    AxiconLens.argtyes = [c_double, c_int, c_int, c_int, c_void_p, c_void_p]
    AxiconLens.restype = c_int
    if(pitch != 0 and pitch != 1):
        print("Error: AxiconLensFunction. invalid argument (pitch).")
        return -1
    # input argument to dll function.
    print(c_int(x*y))
    AxiconLens(c_double(top), pitch, x, y, byref(c_int(x*y)), byref(array))
    return 0

# Display axiconLens pattern array with using dll 生成axicon 相位图
top = 10.0 #top level，中间圆环是几个像素大小
makeAxiconLensArray(top, pitch, x, y, farray)
# 将产生的相位图，显示在SLM上。
showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, farray)






