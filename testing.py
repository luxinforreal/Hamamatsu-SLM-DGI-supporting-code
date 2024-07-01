import ctypes
dll = ctypes.cdll.LoadLibrary("D:/Github/Hamamatsu-SLM-DGI-supporting-code/Image_Control.dll")
functions = dir(dll)
for function in functions:
    print(function)