# -*- coding: utf-8 -*-
"""
Created on Sat May  6 11:51:25 2023

@author: odink
"""

import os
import numpy as np
import open3d as o3d

# Define the path to the PLY file
#ply_file_path = './merged_point_clouds/merged_and_trimmed_final/map_from_dataset_depth.ply'
ply_file_path = './merged_point_clouds/merged_and_trimmed_final/map_from_dataset_depth.ply'

# Define the directory where the layer files will be saved
save_to_directory = './merged_point_clouds/layers'


pcd = o3d.io.read_point_cloud(ply_file_path)
num_layers = 20


max_y = pcd.get_max_bound()[1]
min_y = pcd.get_min_bound()[1]

# Calculate the height of each layer
layer_height = (max_y - min_y) / num_layers

# Loop through each layer and extract the points that fall within its y-range
layers = []
for i in range(num_layers):
    layer_min_y = min_y + i * layer_height
    layer_max_y = min_y + (i + 1) * layer_height
    indices = []
    for j, point in enumerate(pcd.points):
        if layer_min_y <= point[1] < layer_max_y:
            indices.append(j)
    layer = pcd.select_by_index(indices)
    o3d.io.write_point_cloud(save_to_directory+"/layers_"+str(i)+".ply",layer)
    layers.append(layer)






