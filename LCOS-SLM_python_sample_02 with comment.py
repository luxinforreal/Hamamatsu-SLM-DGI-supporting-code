# -*- coding: utf-8 -*-
"""
Created on Mon May 18 14:10:00 2020

@author: HPK
"""
#初步的模块导入包括PIL numpy需要客户自己安装
from PIL import Image
import numpy as np
from ctypes import *
import copy
'''
以下是主函数，内部包含了许多具体的功能，实际测试的时候，只要把其中某个功能给提出来就可以了。然后需要把后面def的那些函数放到前面。
'''
def main():

    #pixelpitch(0: 20um 1: 12.5um)
    pitch = 1
    
    #LCOS pixel resolution 设置SLM的分辨率。
    x = 1272
    y = 1024
    
    #LCOS-SML monitor number setting 如果只连接一个SLM默认monitorNo=2, windowNo=0
    monitorNo = 2
    windowNo = 0
    xShift = 0
    yShift = 0
    
    #pixel number 总共像素的个数，方便后面函数调用
    array_size = x * y

    # make the 8bit unsigned integer array type 初始化用于存储相位图,结果是_ctypes.PyCArrayType
    FARRAY = c_uint8 * array_size

    # make the 8bit unsigned integer array instance
    farray = FARRAY(0) #类型是<class '__main__.c_ubyte_Array_1310720'> c_ubyte是 unsigned char ，然后这是一个矩阵，大小是1*array_size
    farray2 = FARRAY(0)
    farray3 = FARRAY(0)
    
    #Display axiconLens pattern array with using dll 生成axicon 相位图
    top = 10.0 #top level，从中间点，到屏幕四个角，是top*pi，比如10的话，那就是总共10pi。
    makeAxiconLensArray(top, pitch, x, y, farray)
    #将产生的相位图，显示在SLM上。
    showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, farray)
    
    #Display cylindricalLens pattern array with using dll 生成柱透镜相位图
    forcus = 1000 #设置焦距是1000mm
    wavelength = 1064 #设置波长是1064nm
    modeSelect = 0 # 0: horizontal or 1: vertical
    makeCylindricalLensArray(forcus, wavelength, pitch, modeSelect, x, y, farray)
    showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, farray)
    
    #Display rotated pattern array with using dll 将相位图旋转ay输入是farray矩阵，输出是farray2矩阵
    degree = 30.0
    imageRotation(farray, degree, x, y, farray2)
    showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, farray2)
    
    #Display diffraction grating pattern array with using dll 生成grating相位图
    rowOrColumn = 0
    gradiationNo = 16
    gradiationWidth = 16
    slipFactor = 0
    makeDiffractionPatternArray(rowOrColumn, gradiationNo, gradiationWidth, slipFactor, x, y, farray)
    showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, farray)
    
    #Display Laguerre Gauss Mode pattern array with using dll 生成拉盖尔高斯光，主要就是涡旋光
    p = 1
    m = 1
    pitch = 1
    beamSize = 20.0
    makeLaguerreGaussModeArray(p, m, pitch, beamSize, x, y, farray)
    showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, farray)
    
    #Display FresnelLens pattern array with using dll  生成菲涅尔透镜相位
    forcus = 1000
    wavelength = 1064
    makeFresnelLensArray(forcus, wavelength, pitch, x, y, farray2)
    showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, farray2)
    
    #Display synthesize FresnelLens and Laguerre Gauss Mode pattern array with using dll  生成叠加了菲涅尔透镜farray2与LG光FARRAY，冰生成farray3相位图
    phaseSynthsizer([farray, farray2], farray3)
    showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, farray3)
 
    #Display CGH pattern from image file with using dll  载入图像，并且计算CGH
    filepath = "Target image sample\\char_hpk_128x128.bmp"
    makeBmpArray(filepath, x, y, farray)
    showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, farray)

    #display image from file with dll. 直接载入计算的相位图
    filepath = "D:\\python_project\\1024.bmp"
    loadBmpArray(filepath, x, y, farray)
    showOn2ndDisplay(monitorNo, windowNo, x, xShift, y, yShift, farray)
    return 0
'''
以下是上面各个功能实现所依赖的函数，在实际使用的时候，需要把他放到前面（import之后）。这些函数结合了dll中的内置函数，和其它一些判断函数组成。
'''


'''
the function for making AxiconLens pattern array
double top: Top level of AxiconLens pattern. (/pi rad)  从相位中心区域，到相位四个角有多少个像素跨度，如果10的话，那就是10pi个跨度
int pitch: Pixel pitch. 0: 20um 1: 12.5um SLM像素尺寸大小
int x: Pixel number of x-dimension
int y: Pixel number of y-dimension
8bit unsigned integer array array: output array
'''
def makeAxiconLensArray(top, pitch, x, y, array):
    #Lcoslib = cdll.LoadLibrary("Image_Control.dll") #for cdll cdll和windll这两个影响不是很大，可以参考网页 https://blog.csdn.net/caimouse/article/details/38395461
    Lcoslib = windll.LoadLibrary("Image_Control.dll") #for windll
    AxiconLens = Lcoslib.AxiconLens #调取imagecontrol.dll中的axiconlens函数
    AxiconLens.argtyes = [c_double, c_int, c_int, c_int, c_void_p, c_void_p] # 设置输入的参数类型，和c语言对应关系可以参考https://blog.csdn.net/wjg1314521/article/details/122350227
    AxiconLens.restype = c_int #设置返回值的参数类型
    if(pitch != 0 and pitch != 1): #判断输入的像素尺寸是否正确
        print("Error: AxiconLensFunction. invalid argument (pitch).")
        return -1
    # input argument to dll function.
    AxiconLens(c_double(top), pitch, x, y, byref(c_int(x*y)), byref(array)) #调用函数，输出的结果在array里，也就是外面调用的farray
    return 0

'''
the function for making CylindricalLens pattern array
int focus: the forcus of cylindrical lens. (mm) 
int wavelength: the wavelength of light. (nm)
int pitch: Pixel pitch. 0: 20um 1: 12.5um
int modeSelect: 0: horizontal or 1: vertical
int x: Pixel number of x-dimension
int y: Pixel number of y-dimension
8bit unsigned int array array: output array
'''
def makeCylindricalLensArray(forcus, wavelength, pitch, modeSelect, x, y, array):
    #Lcoslib = cdll.LoadLibrary("Image_Control.dll") #参见makeAxiconLensArray部分的解释
    Lcoslib = windll.LoadLibrary("Image_Control.dll")
    CylindricalLens = Lcoslib.CylindricalLens #调用imagecontrol.dll中的CylindricalLens函数
    CylindricalLens.argtyes = [c_int, c_int, c_int, c_int, c_int, c_int, c_void_p, c_void_p] ## 设置输入的参数类型，和c语言对应关系可以参考https://blog.csdn.net/wjg1314521/article/details/122350227
    CylindricalLens.restype = c_int #设置返回参数类型
    if(pitch != 0 and pitch != 1):   #判断输入的像素尺寸是否正确
        print("Error: CylindricalLensFunction. invalid argument (pitch).")
        return -1
    CylindricalLens(forcus, wavelength, pitch, modeSelect, x, y, byref(c_int(x*y)), byref(array)) #调用函数
    return 0

'''
the function for making Diffraction pattern array
int rowOrColumn: 0: horizontal or 1: vertical
int gradiationNo: the number of gradiation.
int gradiationWidth: the width of gradiation.
int slipFactor: slip factor.
int x: Pixel number of x-dimension
int y: Pixel number of y-dimension
8bit unsigned int array array: output array
'''
def makeDiffractionPatternArray(rowOrColumn, gradiationNo, gradiationWidth, slipFactor, x, y, array):
    #Lcoslib = cdll.LoadLibrary("Image_Control.dll")
    Lcoslib = windll.LoadLibrary("Image_Control.dll")
    Diffraction_pattern = Lcoslib.Diffraction_pattern
    Diffraction_pattern.argtyes = [c_int, c_int, c_int, c_int, c_int, c_int, c_void_p, c_void_p]
    Diffraction_pattern.restype = c_int
    Diffraction_pattern(rowOrColumn, gradiationNo, gradiationWidth, slipFactor, x, y, byref(c_int(x*y)), byref(array))
    return 0

'''
the function for making LaguerreGaussMode pattern array
int p: radial index
int m: azimuthal index 
int pitch: Pixel pitch. 0: 20um 1: 1.25um
double beamSize: Beam size (mm)
int x: Pixel number of x-dimension
int y: Pixel number of y-dimension
8bit unsigned int array array: output array
'''
def makeLaguerreGaussModeArray(p, m, pitch, beamSize, x, y, array):
    #Lcoslib = cdll.LoadLibrary("Image_Control.dll")
    Lcoslib = windll.LoadLibrary("Image_Control.dll")
    LaguerreGaussMode = Lcoslib.LaguerreGaussMode
    LaguerreGaussMode.argtyes = [c_int, c_int, c_int, c_double, c_int, c_int, c_void_p, c_void_p]
    LaguerreGaussMode.restype = c_int
    if(pitch != 0 and pitch != 1):
        print("Error: LaguerreGaussModeFunction. invalid argument (pitch).")
        return -1
    LaguerreGaussMode(p, m, pitch, c_double(beamSize), x, y, byref(c_int(x*y)), byref(array))
    return 0

'''
the function for making FresnelLens pattern array
int focus: the forcus of cylindrical lens. (mm)
int wavelength: the wavelength of light. (nm)
int pitch: Pixel pitch. 0: 20um 1: 1.25um
int x: Pixel number of x-dimension
int y: Pixel number of y-dimension
8bit unsigned int array array: output array
'''
def makeFresnelLensArray(forcus, wavelength, pitch, x, y, array):
    #Lcoslib = cdll.LoadLibrary("Image_Control.dll")
    Lcoslib = windll.LoadLibrary("Image_Control.dll")
    FresnelLens = Lcoslib.FresnelLens
    FresnelLens.argtyes = [c_int, c_int, c_int, c_int, c_int, c_int, c_void_p, c_void_p]
    FresnelLens.restype = c_int
    if(pitch != 0 and pitch != 1):
        print("Error: FresnelLensFunction. invalid argument (pitch).")
        return -1
    FresnelLens(forcus, wavelength, pitch, x, y, byref(c_int(x*y)), byref(array))
    return 0

'''
the function for generating cgh image of import image  and load it into farray for showOn2ndDisplay usage
String filepath: image file path.
int x: Pixel number of x-dimension
int y: Pixel number of y-dimension
8bit unsigned int array outArray: output array
'''
def makeBmpArray(filepath, x, y, outArray):
    im = Image.open(filepath)#打开图像，利用的是PIL模块
    imageWidth, imageHeight = im.size #获得打开图像的尺寸，第一个结果是width，第二个结果是height
    im_gray = im.convert("L") #将打开图像转化为8bit灰度图

    print("Imagesize = {} x {}".format(imageWidth, imageHeight)) #输出图像的尺寸，以保证图像打开正确 1272*1024，表示宽是1272，高是1024

    for i in range(imageWidth):
        for j in range(imageHeight):
            outArray[i + imageWidth * j] = im_gray.getpixel((i, j)) #将结果矩阵的结果导入到outarray（实参），也就是farray（形参）中,载入了之后，outarray是C_ubite格式，就是unsigned char,而其中一个元素是int格式

    # Lcoslib = cdll.LoadLibrary("Image_Control.dll")
    Lcoslib = windll.LoadLibrary("D:\\python_project\\Image_Control.dll") #载入dll文件，方便处理
    # #
    # Create CGH
    inArray = copy.deepcopy(outArray) #完成深度拷贝，将outarray复制到inarray
    Create_CGH_OC = Lcoslib.Create_CGH_OC #引用imagecontrol.dll中的CREATE_CGH_OC函数
    Create_CGH_OC.argtyes = [c_void_p, c_int, c_int, c_int, c_int, c_void_p, c_void_p]  #设置输入的参数
    Create_CGH_OC.restype = c_int #设置返回值的参数

    repNo = 100  #设置迭代的次数
    progressBar = 1  #产生进度条，这个就是1就行了
    Create_CGH_OC(byref(inArray), repNo, progressBar, imageWidth, imageHeight, byref(c_int(imageHeight * imageWidth)),
                  byref(outArray))

    # # Tilling the image
    inArray = copy.deepcopy(outArray) #将outarray深度拷贝到inarray中
    Image_Tiling = Lcoslib.Image_Tiling #获取ImageControl.dll中的Image_Tiling函数
    Image_Tiling.argtyes = [c_void_p, c_int, c_int, c_int, c_int, c_int, c_void_p, c_void_p] #设置使用函数的参数，其中C_void_p对应的是C语言中的void *指针，特点是任何类型的指针都可以直接赋值给它，无需进行强制类型转换。
    Image_Tiling.restype = c_int #设置函数的返回值类型

    Image_Tiling(byref(inArray), imageWidth, imageHeight, imageHeight * imageWidth, x, y, byref(c_int(x * y)),
                 pointer(outArray)) #执行函数，通过byref实现的指针，然后是相当于用inarray参数，输出实现了outarray参数。这个地方byref不用也可以，python会自动加上，成为指针。也可以改为使用pointer

    return 0

'''
the function for loading BMP files (calcluated CGH image by the cusomter) into farray for showOn2ndDisplay usage.
String filepath: image file path.
int x: Pixel number of x-dimension
int y: Pixel number of y-dimension
8bit unsigned int array outArray: output array
'''
def loadBmpArray(filepath, x, y, outArray):
    im = Image.open(filepath)#打开图像，利用的是PIL模块
    imageWidth, imageHeight = im.size #获得打开图像的尺寸，第一个结果是width，第二个结果是height
    im_gray = im.convert("L") #将打开图像转化为8bit灰度图

    print("Imagesize = {} x {}".format(imageWidth, imageHeight)) #输出图像的尺寸，以保证图像打开正确 1272*1024，表示宽是1272，高是1024

    for i in range(imageWidth):
        for j in range(imageHeight):
            outArray[i + imageWidth * j] = im_gray.getpixel((i, j)) #将结果矩阵的结果导入到outarray（实参），也就是farray（形参）中

    # Lcoslib = cdll.LoadLibrary("Image_Control.dll")
    Lcoslib = windll.LoadLibrary("D:\\python_project\\Image_Control.dll") #载入dll文件，方便处理
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
    inArray = copy.deepcopy(outArray) #将outarray深度拷贝到inarray中
    Image_Tiling = Lcoslib.Image_Tiling #获取ImageControl.dll中的Image_Tiling函数
    Image_Tiling.argtyes = [c_void_p, c_int, c_int, c_int, c_int, c_int, c_void_p, c_void_p] #设置使用函数的参数，其中C_void_p对应的是C语言中的void *指针，特点是任何类型的指针都可以直接赋值给它，无需进行强制类型转换。
    Image_Tiling.restype = c_int #设置函数的返回值类型

    Image_Tiling(byref(inArray), imageWidth, imageHeight, imageHeight * imageWidth, x, y, byref(c_int(x * y)),
                 pointer(outArray)) #执行函数，通过byref实现的指针，然后是相当于用inarray参数，输出实现了outarray参数。这个地方byref不用也可以，python会自动加上，成为指针。也可以改为使用pointer

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
    Window_Term.argtyes = [c_int]
    Window_Term.restype = c_int
    Window_Term(windowNo)
    
    return 0

'''
the function for Srotating image
input 1D array inputArray: input array. 
double degree: rotation degree (deg.)
int x: Pixel number of x-dimension
int y: Pixel number of y-dimension
output 1D array outputArray: output array. 
'''  
def imageRotation(inputArray, degree, x, y, outputArray):
    #Lcoslib = cdll.LoadLibrary("Image_Control.dll")
    Lcoslib = windll.LoadLibrary("Image_Control.dll")
    
    Image_Rotation = Lcoslib.Image_Rotation
    Image_Rotation.argtyes = [c_void_p, c_double, c_int, c_int, c_void_p, c_void_p]
    Image_Rotation.restype = c_int
    Image_Rotation(byref(inputArray), c_double(degree), x, y, byref(c_int(x*y)), byref(outputArray))
    
    return 0

'''
the function for Synthesizing image pattaerns
input arrays 2D array inputPatterns: the compornents will be synthesized.
output 1D array outputArray: output array. 
'''  
def phaseSynthsizer(inputPatterns, outputArray):
    n = len(inputPatterns[0])
    outputPattern = np.zeros(n, dtype=int)
    for pattern in inputPatterns:
        outputPattern = outputPattern + pattern
    
    for i in range(n):
        outputArray[i] = c_uint8(outputPattern[i] % 256)    
    
    return 0
    
main()
