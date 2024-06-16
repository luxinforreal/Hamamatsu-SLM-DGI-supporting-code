import os
from PIL import Image
# from constants import Constants

def resize_images(input_directory, output_directory, new_size):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for filename in os.listdir(input_directory):
        if filename.endswith(".png"):
            filepath = os.path.join(input_directory, filename)
            with Image.open(filepath) as img:
                resized_img = img.resize(new_size, Image.ANTIALIAS)
                
                output_filepath = os.path.join(output_directory, filename)
                resized_img.save(output_filepath)
                
                print(f"Resized and saved {filename} to {output_filepath}")


def resize_images2(input_directory, new_size):
    for filename in os.listdir(input_directory):
        if filename.endswith(".png"):
            filepath = os.path.join(input_directory, filename)
            temp_filepath = filepath + '.png'
            
            with Image.open(filepath) as img:
                resized_img = img.resize(new_size, resample=Image.Resampling.LANCZOS)
                resized_img.save(temp_filepath)
                
            os.replace(temp_filepath, filepath) 
            print(f"Resized and replaced {filename}")

# input_directory = "C:/Users/allen/Desktop/Hamamatsu-SLM-DGI-supporting-code/test/test-folder-1-png"
# output_directory = "C:/Users/allen/Desktop/Hamamatsu-SLM-DGI-supporting-code/test/test-folder-1-png"
# new_size = (1280, 1024)  

# resize_images(input_directory, output_directory, new_size)



input_directory = "C:/Users/allen/Desktop/Hamamatsu-SLM-DGI-supporting-code/test/test-folder-10-pngs"
new_size = (1280, 1024)  # 设置你想要的尺寸
resize_images2(input_directory, new_size)
