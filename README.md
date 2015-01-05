pixld
=====

usage: pixld.py [-h] [--width WIDTH] [--height HEIGHT] input tiles output

Create a mosaic out of a set of images and a base image.

positional arguments:
  input            the base image for the mosaic
  tiles            the directory containing the images to use as tiles in the
                   mosaic
  output           the output image of the mosaic

optional arguments:
  -h, --help       show this help message and exit
  --width WIDTH    the width of a tile in the mosaic (default: 20 pixels)
  --height HEIGHT  the height of a tile in the mosaic (default: 20 pixels)
