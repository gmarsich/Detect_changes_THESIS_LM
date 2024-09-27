'''This script takes in input the set of .ply files (each one containing an instance) and generates a unique .ply file such
that its beginning appears like this:

ply
format ascii 1.0
element vertex 1796927
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
property int objectId
end_header
6.026266 -5.158844 -1.588580 68 32 130 0
6.016451 -5.158467 -1.589023 68 32 130 0

'''

# environment: sceneGraphs_Gaia

import numpy as np
import os
import open3d as o3d
import glob


#
# Variables
#

base_path_instancePCDs = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/Segmentation'
path_save_newPCD = '/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/withPCA/preprocessing/results/frl_apartment_1_withIDs.ply'

path_transformationMatrix = '/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/sgaligner_MOD_Replica/0GAIA/alignment_Replica/results_alignment/frl_apartment_1_to_frl_apartment_0/frl_apartment_1_to_frl_apartment_0.txt'
usingTarget = False # True: the .ply is the target: don't apply the transformation; False: the transformation has to be performed


#
# Get the list of paths leading to the mesh_semantic.ply_i.ply files
#

pattern = os.path.join(base_path_instancePCDs, 'mesh_semantic.ply_*')
file_paths = glob.glob(pattern) # CAVEAT: the list is not ordered following the names of the meshes


#
# Load all the instances, get for each the ID, save to a .ply file the entire point cloud
#

transformation_matrix = np.loadtxt(path_transformationMatrix)


def get_data_for_pointCloud(file_paths, usingTarget):
    all_points = []
    all_colors = []
    all_object_ids = []

    for path in file_paths:
        filename = os.path.basename(path)
        parts = filename.split('.')

        objectID = int(parts[1].split('_')[1])
        
        if os.path.exists(path):
            pcd = o3d.io.read_point_cloud(path)
            if not usingTarget:
                pcd.transform(transformation_matrix)

            points = np.asarray(pcd.points)
            colors_normalised = np.asarray(pcd.colors)
            colors = (colors_normalised * 255).astype(np.uint8)
            object_IDs = np.full((points.shape[0], 1), objectID)

            all_points.append(points)
            all_colors.append(colors)
            all_object_ids.append(object_IDs)

    all_points = np.vstack(all_points)
    all_colors = np.vstack(all_colors)
    all_object_ids = np.vstack(all_object_ids)

    return all_points, all_colors, all_object_ids


points, colors, object_ids = get_data_for_pointCloud(file_paths, usingTarget)
combined_data = np.hstack((points, colors, object_ids))

# Write the PLY file manually
with open(path_save_newPCD, 'w') as f:
    # Write PLY header
    f.write("ply\n")
    f.write("format ascii 1.0\n")
    f.write(f"element vertex {combined_data.shape[0]}\n")
    f.write("property float x\n")
    f.write("property float y\n")
    f.write("property float z\n")
    f.write("property uchar red\n")
    f.write("property uchar green\n")
    f.write("property uchar blue\n")
    f.write("property int objectId\n")
    f.write("end_header\n")

    # Write point data
    for point in combined_data:
        f.write(f"{point[0]:.6f} {point[1]:.6f} {point[2]:.6f} {int(point[3])} {int(point[4])} {int(point[5])} {int(point[6])}\n")

colored_point_cloud = o3d.io.read_point_cloud(path_save_newPCD)
o3d.visualization.draw_geometries([colored_point_cloud])



