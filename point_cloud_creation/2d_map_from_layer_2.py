# -*- coding: utf-8 -*-
"""
Created on Sat May  6 20:12:07 2023

@author: odink
"""

import open3d as o3d
import numpy as np
from PIL import Image


#directory containing target point cloud 
pcd = o3d.io.read_point_cloud("./merged_point_clouds/layer_best/layers_11_maybe_dataset.ply")

x_coords = np.asarray(pcd.points)[:, 0] * 100000
z_coords = np.asarray(pcd.points)[:, 2] * 100000

min_x, max_x = np.min(x_coords), np.max(x_coords)
min_z, max_z = np.min(z_coords), np.max(z_coords)

img_width, img_height = int(max_x - min_x + 1), int(max_z - min_z + 1)
img = np.zeros((img_height, img_width))

for i in range(len(x_coords)):
    x = int(x_coords[i] - min_x)
    z = int(max_z - z_coords[i])
    img[z, x] = 1


#save resulting image to specified directory 
Image.fromarray((img * 255).astype(np.uint8)).save("./2d_maps/layer_11_dataset_2.png")