# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:17:34 2023

@author: odink
"""

from PIL import Image

image = Image.open("./2d_maps/layer_11_ours_2_enhanced.png")

# Convert the image to grayscale
gray_image = image.convert("L")

# Get the pixel data as a list of values
pixel_data = list(gray_image.getdata())

# Convert the pixel values to -1 for white and 1 for black
binary_data = [1 if pixel < 10 else -1 for pixel in pixel_data]

# Write the binary data to a CSV file
with open("./layer_11_ours_2_enhanced.csv", "w") as csv_file:
    for i in range(0, len(binary_data), gray_image.width):
        row = binary_data[i:i + gray_image.width]
        csv_file.write(",".join([str(pixel) for pixel in row]) + "\n")