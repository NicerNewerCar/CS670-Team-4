# -*- coding: utf-8 -*-
"""
Created on Fri May  5 17:34:17 2023

@author: odink
"""

import open3d as o3d
import numpy as np





for i in range(0,280):#how many point clouds to remove outliers from
    pcd = o3d.io.read_point_cloud("./pcd_basement_ours/pcd_"+str(i)+".ply")#target point cloud
    
    #pcd = pcd.voxel_down_sample(voxel_size=0.000006)
    
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=0.5)
    inlier_cloud = pcd.select_by_index(ind)
    o3d.io.write_point_cloud("./pcd_basement_ours/outlier_removed/all_stat_nb_20_ratio_0-5/pcd_"+str(i)+".ply", inlier_cloud)#destination of resulting point cloud