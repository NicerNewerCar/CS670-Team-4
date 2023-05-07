# -*- coding: utf-8 -*-
"""
Created on Fri May  5 16:40:44 2023


most of this is from here made minor adjustments
http://www.open3d.org/docs/latest/tutorial/Advanced/multiway_registration.html
"""

import open3d as o3d
import numpy as np


to_merge1 = "./pcd_basement_dataset/pcd_%d.pcd"
to_merge2 = "./pcd_outlier_basement_dataset/first_30_stat_nb_20_ratio_0-05/pcd_%d.pcd"
to_merge3 = "./pcd_outlier_basement_dataset/first_30_stat_nb_10_ratio_0-01/pcd_%d.pcd"
to_merge4 = "./pcd_outlier_basement_dataset/second_30_stat_nb_20_ratio_0-05/pcd_%d.pcd"
merge_30  = "./merged_point_clouds/merged_and_trimmed/"
merge_all = "./pcd_outlier_basement_dataset/all_stat_nb_20_ratio_0-05/pcd_%d.pcd"
merge_all2= "./pcd_outlier_basement_dataset/all_stat_nb_20_ratio_0-5/pcd_%d.pcd"
merge_all3= "./pcd_basement_ours/outlier_removed/all_stat_nb_20_ratio_0-5/pcd_%d.ply"

def display_inlier_outlier(cloud, ind):
    inlier_cloud = cloud.select_by_index(ind)
    outlier_cloud = cloud.select_by_index(ind, invert=True)
    o3d.visualization.draw_geometries([inlier_cloud])
    o3d.io.write_point_cloud("./pcd_basement_ours/outlier_removed/ours_merged/1_0-30.ply", inlier_cloud)



def load_point_clouds(voxel_size=0.0):
    pcds = []
    for i in range(0,30,2):
        
        pcd = o3d.io.read_point_cloud(merge_all3 %i)
        #o3d.visualization.draw_geometries([pcd]) 
        pcd.estimate_normals()
        pcd_down = pcd.voxel_down_sample(voxel_size=voxel_size)
        #got rid of down sample
        pcds.append(pcd_down)
    return pcds

def pairwise_registration(source, target):
    print("Apply point-to-plane ICP")
    icp_coarse = o3d.pipelines.registration.registration_icp(
        source, target, max_correspondence_distance_coarse, np.identity(4),
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    icp_fine = o3d.pipelines.registration.registration_icp(
        source, target, max_correspondence_distance_fine,
        icp_coarse.transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    transformation_icp = icp_fine.transformation
    information_icp = o3d.pipelines.registration.get_information_matrix_from_point_clouds(
        source, target, max_correspondence_distance_fine,
        icp_fine.transformation)
    return transformation_icp, information_icp


def full_registration(pcds, max_correspondence_distance_coarse,
                      max_correspondence_distance_fine):
    pose_graph = o3d.pipelines.registration.PoseGraph()
    odometry = np.identity(4)
    pose_graph.nodes.append(o3d.pipelines.registration.PoseGraphNode(odometry))
    n_pcds = len(pcds)
    for source_id in range(n_pcds):
        for target_id in range(source_id + 1, n_pcds):
            transformation_icp, information_icp = pairwise_registration(
                pcds[source_id], pcds[target_id])
            print("Build o3d.pipelines.registration.PoseGraph")
            if target_id == source_id + 1:  # odometry case
                odometry = np.dot(transformation_icp, odometry)
                pose_graph.nodes.append(
                    o3d.pipelines.registration.PoseGraphNode(
                        np.linalg.inv(odometry)))
                pose_graph.edges.append(
                    o3d.pipelines.registration.PoseGraphEdge(source_id,
                                                             target_id,
                                                             transformation_icp,
                                                             information_icp,
                                                             uncertain=False))
            else:  # loop closure case
                pose_graph.edges.append(
                    o3d.pipelines.registration.PoseGraphEdge(source_id,
                                                             target_id,
                                                             transformation_icp,
                                                             information_icp,
                                                             uncertain=True))
    return pose_graph


#voxel_size2 = 0.000025
#voxel_size  = 0.00001
#voxel_size  = 0.000006
voxel_size   = 0.0000001 
pcds_down = load_point_clouds(voxel_size)
#"""
o3d.visualization.draw_geometries(pcds_down)
#"""


print("Full registration ...")
max_correspondence_distance_coarse = voxel_size * 15
max_correspondence_distance_fine = voxel_size * 1.5
with o3d.utility.VerbosityContextManager(
        o3d.utility.VerbosityLevel.Debug) as cm:
    pose_graph = full_registration(pcds_down,
                                   max_correspondence_distance_coarse,
                                   max_correspondence_distance_fine)

print("Optimizing PoseGraph ...")
option = o3d.pipelines.registration.GlobalOptimizationOption(
    max_correspondence_distance=max_correspondence_distance_fine,
    edge_prune_threshold=0.25,
    reference_node=0)
with o3d.utility.VerbosityContextManager(
        o3d.utility.VerbosityLevel.Debug) as cm:
    o3d.pipelines.registration.global_optimization(
        pose_graph,
        o3d.pipelines.registration.GlobalOptimizationLevenbergMarquardt(),
        o3d.pipelines.registration.GlobalOptimizationConvergenceCriteria(),
        option)


print("Transform points and display")
for point_id in range(len(pcds_down)):
    print(pose_graph.nodes[point_id].pose)
    pcds_down[point_id].transform(pose_graph.nodes[point_id].pose)
"""
o3d.visualization.draw_geometries(pcds_down,
                                  zoom=0.3412,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                 up=[-0.0694, -0.9768, 0.2024])
"""

pcds = load_point_clouds(voxel_size)
pcd_combined = o3d.geometry.PointCloud()
for point_id in range(len(pcds)):
    pcds[point_id].transform(pose_graph.nodes[point_id].pose)
    pcd_combined += pcds[point_id]
pcd_combined_down = pcd_combined.voxel_down_sample(voxel_size=voxel_size)
#o3d.io.write_point_cloud("./merged_point_clouds/test_2/first60_nb_20_ratio_0-5_every_2nd.pcd", pcd_combined_down)
#o3d.visualization.draw_geometries([pcd_combined_down])
o3d.visualization.draw_geometries([pcd_combined_down])                                

pcd_combined_down = pcd_combined_down.voxel_down_sample(voxel_size=0.000006)
cl, ind = pcd_combined_down.remove_statistical_outlier(nb_neighbors=20, std_ratio=0.5)                             
display_inlier_outlier(pcd_combined_down, ind)
#o3d.visualization.draw_geometries([pcd_combined_down])                                
                             
                                
                             
                                
                             
                                
                             
                                
                             
                                
                             
                                

