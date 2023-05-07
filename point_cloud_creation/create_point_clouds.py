# -*- coding: utf-8 -*-
"""
Created on Fri May  5 14:18:22 2023

@author: odink
"""

import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from PIL import Image
import torch
from transformers import GLPNImageProcessor, GLPNForDepthEstimation
import numpy as np
import open3d as o3d
import cv2


rgb_path   = "./rgb_depth_ours/rgb"
depth_path = "./rgb_depth_ours/depth_map"

def main():
    
    # camera settings
    camera_intrinsic = o3d.camera.PinholeCameraIntrinsic()
    
    for i in range(0,281):
        rgb = Image.open(rgb_path+str(i)+".png")
        depth = Image.open(depth_path+str(i)+".png")
        #rgb= rgb.resize(target_size)#depth maps made by side are smaller
            
        width, height = rgb.size
    
        depth = np.array(depth)
    
        depth = depth.astype(np.float32)

        depth_image = (depth * 255 / np.max(depth)).astype('uint8')
        rgb = np.array(rgb)

        # create rgbd image
        depth_o3d = o3d.geometry.Image(depth_image)
        image_o3d = o3d.geometry.Image(rgb)      
        rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(image_o3d, depth_o3d, convert_rgb_to_intensity=False)
    
        # camera settings
        camera_intrinsic.set_intrinsics(width, height, 500, 500, width/2, height/2)

        # create point cloud
        pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, camera_intrinsic)
        
        o3d.io.write_point_cloud("./pcd_basement_ours/pcd_"+str(i)+".ply", pcd)
        
        #o3d.visualization.draw_geometries([pcd])


if __name__ == '__main__':
    main()
    
    
    
    
    