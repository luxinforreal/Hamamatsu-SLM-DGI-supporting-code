import numpy as np
from PIL import Image
import os

img_W = 1280
img_H = 1024
image_dir = 'C:/Users/allen/Desktop/Hamamatsu-SLM-DGI-supporting-code/test/test-folder-Mathiue-10-bmps/'  # 替换为你的图像目录路径
new_image_dir = 'C:/Users/allen/Desktop/Hamamatsu-SLM-DGI-supporting-code/test/temp/'  # 替换为你想保存新图像的目录路径

for i in range(10):
    image_path = image_dir + '%d.bmp' % (i+1)
    # 打开图像文件
    img = Image.open(image_path)
    # 转换为灰度图像
    img_gray = img.convert('L')
    # 重新调整图像大小
    resized_img = img_gray.resize((img_W, img_H))
    # 保存调整大小后的图像覆盖原文件
    new_image_path = os.path.join(new_image_dir, f'{i+1}.bmp') 
    resized_img.save(new_image_dir)
    print(f"Processed and saved image {i+1} to {new_image_dir}")
    print(i)

print("All images have been resized and saved.")