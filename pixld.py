import argparse
import collections
import os
import random 
from PIL import Image

background_file = 'awesome.jpg'
image_dir = 'images'
target_dir = 'output.jpg'
pixel_size = (50, 50)

def get_average_color(image):
    pixel_sum = map(sum, zip(*image.getdata()))
    return tuple(value / (image.size[0] * image.size[1]) for value in pixel_sum)

def square(image, size):
    return image.crop((0, 0, min(image.size), min(image.size))).resize(size) 

images = [square(Image.open(os.path.join(image_dir, i)), pixel_size) for i in os.listdir(image_dir)]
color_map = collections.defaultdict(list)

for image in images:
    color_map[get_average_color(image)].append(image)

background = Image.open(background_file)
new_image = Image.new('RGB', (background.size[0]*pixel_size[0], background.size[1]*pixel_size[1])) 

for i in range(background.size[0]):
    for j in range(background.size[1]):
        target = background.getpixel((i, j))
        image = random.choice(color_map[min(color_map.keys(), key=lambda color: sum(abs(c[0] - c[1]) for c in zip(color, target)))])
        new_image.paste(image, (pixel_size[0] * i, pixel_size[1] * j))

new_image.save('output.jpg')
