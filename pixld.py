#!/usr/bin/python
import argparse
import collections
import os
import random
from PIL import Image


def get_average_color(image):
    pixel_sum = map(sum, zip(*image.getdata()))
    num_pixels = image.size[0] * image.size[1]
    return tuple(value / num_pixels for value in pixel_sum)


def square(image, size):
    small_dim = min(image.size)
    return image.crop((0, 0, small_dim, small_dim)).resize(size)


parser = argparse.ArgumentParser(
    description='Create a mosaic out of a set of images and a base image.')
parser.add_argument('input',
                    help='the base image for the mosaic')
parser.add_argument('tiles',
                    help='the directory containing the images'
                    ' to use as tiles in the mosaic')
parser.add_argument('output',
                    help='the output image of the mosaic')
parser.add_argument('-v', action='store_true',
                    help='turn on verbose mode')
parser.add_argument('--width', default=20,
                    help='the width of a tile in the mosaic'
                    ' (default: 20 pixels)')
parser.add_argument('--height', default=20,
                    help='the height of a tile in the mosaic'
                    ' (default: 20 pixels)')

args = parser.parse_args()
size = (args.width, args.height)
images = [square(Image.open(os.path.join(args.tiles, i)), size)
          for i in os.listdir(args.tiles)]
color_map = collections.defaultdict(list)

if args.v: print 'Calculating average colors for tiles...'

for image in images:
    color_map[get_average_color(image)].append(image)

if args.v: print 'Opening base image...'

background = Image.open(args.input)

if args.v: print 'Creating output image...'

new_image = Image.new(
    'RGB', (background.size[0] * args.width, background.size[1] * args.height))

for i in range(background.size[0]):

    if args.v: print 'Selecting tiles for row {0}/{1}...'.format(i+1, background.size[0])

    for j in range(background.size[1]):
        target = background.getpixel((i, j))
        image = random.choice(color_map[min(color_map.keys(), key=lambda color:
                                        sum(abs(c[0] - c[1]) for c in
                                        zip(color, target)))])
        new_image.paste(image, (args.width * i, args.height * j))

if args.v: print 'Outputting final image...'

new_image.save(args.output)
