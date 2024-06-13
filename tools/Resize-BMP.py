import os
from PIL import Image

def resize_images(input_directory, output_directory, new_size):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for filename in os.listdir(input_directory):
        if filename.endswith(".bmp"):
            filepath = os.path.join(input_directory, filename)
            with Image.open(filepath) as img:
                resized_img = img.resize(new_size, Image.ANTIALIAS)
                
                output_filepath = os.path.join(output_directory, filename)
                resized_img.save(output_filepath)
                
                print(f"Resized and saved {filename} to {output_filepath}")

# 示例用法
input_directory = "test/test-folder-1-bmp"  
output_directory = "test/test-folder-1-bmp"  
new_size = (1280, 1024)  

resize_images(input_directory, output_directory, new_size)
