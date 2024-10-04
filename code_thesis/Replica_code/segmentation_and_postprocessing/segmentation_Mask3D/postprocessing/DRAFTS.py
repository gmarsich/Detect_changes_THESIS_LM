import open3d as o3d

colored_point_cloud = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/frl_apartment_0_withIDs.ply')
colored_point_cloud_2 = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/frl_apartment_1_withIDs.ply')
o3d.visualization.draw_geometries([colored_point_cloud_2, colored_point_cloud])

# # print(f"First point: {colored_point_cloud.points[0]}")


# # from plyfile import PlyData

# # n_lines = 10

# # # Path to your PLY file
# file_path = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/scannet200_mask3d_1/mesh_labelled.ply'
# # with open(file_path, 'rb') as ply_file:  # Open the file in binary mode
# #     plydata = PlyData.read(ply_file)

# # # Print the header information
# # print(plydata)


# colored_point_cloud = o3d.io.read_point_cloud(file_path)
# print(len(colored_point_cloud.points))

# # Path to your text file
# file_path = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/scannet200_mask3d_1/pred_mask/000.txt'

# # Initialize a counter for the number of lines
# line_count = 0

# # Open the file in read mode and count the lines
# with open(file_path, 'r') as file:
#     for line in file:
#         line_count += 1

# print(f'The file contains {line_count} lines.')


import os
import numpy as np
import open3d as o3d

#
# Variables to set
#

frl_apartment = 'frl_apartment_3'
pcd_mask3D = o3d.io.read_point_cloud('/local/home/gmarsich/Desktop/data_Replica/frl_apartment_3/scannet200_mask3d_1/mesh_labelled.ply')
path_folderResults = '/local/home/gmarsich/Desktop/data_Replica' # if the folder does not exist, it will be created

#
# Automatic variables, in theory they are ok like this
#

path_mask3d_folder = os.path.join(path_folderResults, frl_apartment, 'scannet200_mask3d_1')

path_pred_mask = os.path.join(path_mask3d_folder, 'pred_mask')
path_predictions = os.path.join(path_mask3d_folder, 'predictions.txt')
path_mesh = os.path.join(path_mask3d_folder, 'mesh_labelled.ply')

current_dir = os.path.dirname(os.path.abspath(__file__))
scannet_file = os.path.join(current_dir, 'scannet200_constants.py')


#
# Aaaaaaaaa
#


def get_instance(path_pred_mask, pcd_mask3D):
    points = np.asarray(pcd_mask3D.points)
    colors = np.asarray(pcd_mask3D.colors)
    with open(path_pred_mask, 'r') as f:
        mask = np.array([int(line.strip()) for line in f])
    assert len(mask) == len(points)
    selected_points = points[mask != 0]
    selected_colors = colors[mask != 0]
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(selected_points)
    point_cloud.colors = o3d.utility.Vector3dVector(selected_colors)
    o3d.visualization.draw_geometries([point_cloud])

    
path_pred_mask = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_3/scannet200_mask3d_1/pred_mask/020.txt'
get_instance(path_pred_mask, pcd_mask3D)
