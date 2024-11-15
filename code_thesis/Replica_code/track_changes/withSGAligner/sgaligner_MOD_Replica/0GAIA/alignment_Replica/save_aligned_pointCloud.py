'''This script get the transformation matrix previously obtained for the alignement, applies it to the source point cloud and save the
modified point cloud.'''

# environment: sgm


import numpy as np
import os
import open3d as o3d
import copy

#
# Variables to set
#

target_name = "frl_apartment_0" # its reference system will be used as world reference system
source_name = "frl_apartment_1" # to be moved according to the world reference system

folder_results = "/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/sgaligner_MOD_Replica/0GAIA/alignment_Replica" # where were the results stored?

pcd_target = o3d.io.read_point_cloud(os.path.join("/local/home/gmarsich/data2TB/DATASETS/Replica/", target_name, "mesh.ply"))
pcd_source = o3d.io.read_point_cloud(os.path.join("/local/home/gmarsich/data2TB/DATASETS/Replica/", source_name, "mesh.ply"))

seeRendering = True # do you want to visualise the point clouds?


#
# Apply the transformation matrix to the source point cloud. Save the aligned point cloud
#

name_results = source_name + "_to_"+ target_name
path_results = os.path.join(folder_results, "results_alignment", name_results)

transformation_matrix = np.loadtxt(os.path.join(path_results, name_results + ".txt"))
pcd_source.transform(transformation_matrix)

if seeRendering:
    source_temp = copy.deepcopy(pcd_source)
    target_temp = copy.deepcopy(pcd_target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    o3d.visualization.draw_geometries([source_temp, target_temp])

o3d.io.write_point_cloud(os.path.join(path_results, source_name + "_ALIGNED_to_" + target_name + ".ply"), pcd_source)
