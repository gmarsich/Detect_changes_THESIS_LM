# environment: sceneGraphs_groundTruth_Replica (yes, the name could have been changed)

'''To retrieve the the segmentation in a scene from the Replica dataset starting from the files generated by LabelMaker.
This code creates three files:
- matrix_distances_file_LabelMaker.txt (in the filename the distance that has been used is specified)
- associations_objectIdIndex_LabelMaker.json (keys are objectIDs, values are the indexes in the distance matrix)
- list_instances_LabelMaker.txt
- colorDict_frlApartments_LabelMaker.json, directly from scannet

Also saves the point cloud with an header similar to this one:

ply
format ascii 1.0
element vertex 1820201
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
property float nx
property float ny
property float nz
property int objectId
end_header
4.310055 -9.044144 0.180156 56 55 78 0.093243 -0.983993 -0.151864 13
4.323123 -9.043898 0.168617 37 33 46 0.108986 -0.992858 0.048523 13

'''

# Had to use in the terminal: export PYTHONNOUSERSITE=True # maybe no

import numpy as np
import os
import open3d as o3d
import json
import time
import copy

from scannet200_constants import VALID_CLASS_IDS_200, CLASS_LABELS_200, SCANNET_COLOR_MAP_200 # local file
from side_code.side_code import * # local file


start_time = time.time()

#
# Variables to set
#

frl_apartment = 'frl_apartment_1'
path_folderResults = '/local/home/gmarsich/Desktop/data_Replica'
chosen_distance = distance_Euclidean_closest_points # be aware that with distance_Euclidean_closest_points a downsampling will be performed
scaling_factor = 50 # for downsampling to perform distance_Euclidean_closest_points
saveColorDict = False # do you need the dictionary with the absolute colors?
path_transformationMatrix = '/local/home/gmarsich/Desktop/data_Replica/results_alignment/frl_apartment_1_to_frl_apartment_0/frl_apartment_1_to_frl_apartment_0.txt'



#
# Automatic variables, in theory they are ok like this
#

path_mask3d_folder = os.path.join(path_folderResults, frl_apartment, 'scannet200_mask3d_1')

path_save_files = os.path.join(path_folderResults, frl_apartment)
path_pred_mask = os.path.join(path_mask3d_folder, 'pred_mask')
path_predictions = os.path.join(path_mask3d_folder, 'predictions.txt')
path_mesh = os.path.join(path_mask3d_folder, 'mesh_labelled.ply')

path_original_pcd = os.path.join('/local/home/gmarsich/data2TB/DATASETS/Replica', frl_apartment, 'mesh.ply')
path_save_newPCD = os.path.join(path_folderResults, frl_apartment, frl_apartment + '_withIDs_LabelMaker.ply')

path_save_colorDict = os.path.join(path_folderResults, 'colorDict_frlApartments_LabelMaker.json')

current_dir = os.path.dirname(os.path.abspath(__file__))
scannet_file = os.path.join(current_dir, 'scannet200_constants.py')



#
# Create dict_info, where keys are IDscene and the values are lists like [IDscannet, pcd, sampled_pcd, label]. Save colorDict_frlApartments_LabelMaker.json 
#

dict_info = {}

with open(path_predictions, 'r') as file:
    for line in file:
        parts = line.strip().split()
        
        filename = parts[0]  # this contains the path
        IDscene = int(os.path.splitext(os.path.basename(filename))[0])  # extract IDscene from filename
        IDscannet = int(parts[1])  # the integer that follows the filename

        dict_info[IDscene] = [IDscannet]


dict_paths_predMask = {int(os.path.splitext(file)[0]): os.path.join(path_pred_mask, file) 
                       for file in sorted(os.listdir(path_pred_mask)) 
                       if os.path.isfile(os.path.join(path_pred_mask, file))}

# Add pcd and sampled_pcd

mesh = o3d.io.read_point_cloud(path_mesh)
points = np.asarray(mesh.points)
colors = np.asarray(mesh.colors)

for key, value in dict_paths_predMask.items():
    selected_points = []
    with open(value, 'r') as mask_file:
        mask_lines = mask_file.readlines()

    if len(mask_lines) != len(points):
        print(f"Warning: Mask has {len(mask_lines)} lines but mesh has {len(points)} points. Skipping this mask.")
    else:
        mask = np.array([int(line.strip()) for line in mask_lines])

        selected_points = points[mask != 0]
        selected_colors = colors[mask != 0] # OBS.: it seems that one may have some points with a color different from the color associated to the instance

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(selected_points)
    pcd.colors = o3d.utility.Vector3dVector(selected_colors)
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30)) # estimate normals. Useful for PCA afterwards # TOSET: in case, change parameters

    dict_info[key].append(pcd)


    sampled_pcd = copy.deepcopy(pcd)
    if len(pcd.points) > scaling_factor*10: # 10 has been chosen empirically, randomly
        num_points = round(len(pcd.points) / scaling_factor)
        sampled_pcd = farthest_point_sampling(pcd, num_points)

    dict_info[key].append(sampled_pcd)


# Add label and save colorDict_frlApartments_LabelMaker.json

valid_class_ids = VALID_CLASS_IDS_200
class_labels = CLASS_LABELS_200

dict_scannet = dict(zip(valid_class_ids, class_labels))


for key, value in dict_info.items():
    dict_info[key].append(dict_scannet[value[0]])



if saveColorDict:

    dict_colorMap_IDs = SCANNET_COLOR_MAP_200

    dict_colorMap = {}

    for key, value in dict_scannet.items():
        dict_colorMap[dict_scannet[key]] = list(dict_colorMap_IDs[key])

    with open(path_save_colorDict, 'w') as json_file:
        json.dump(dict_colorMap, json_file, indent=4)



#
# Compute and save the files that are required
#
    
matrix = compute_distance_matrix(dict_info, path_save_files, compute_distance = chosen_distance)



#
# Get the point cloud with the nice header, and with the alignment!
# Note that Mask3D / LabelMaker does not keep everything from the initial point cloud. Therefore, I added a objectID -1 to retrieve the points that
# do not belong to any pred_mask
#

if path_transformationMatrix:
    transformation_matrix = np.loadtxt(path_transformationMatrix) # it is 4x4

all_points = []
all_colors = []
all_normals = []
all_object_ids = []

for key, value in dict_info.items():
    points = np.asarray(dict_info[key][1].points)
    colors_normalised = np.asarray(dict_info[key][1].colors)
    colors = (colors_normalised * 255).astype(np.uint8)
    normals = np.asarray(dict_info[key][1].normals)
    object_IDs = np.full((points.shape[0], 1), key)

    all_points.append(points)
    all_colors.append(colors)
    all_normals.append(normals)
    all_object_ids.append(object_IDs)


# Retrieve the missing points

original_pcd = o3d.io.read_point_cloud(path_original_pcd)
original_pcd_points = np.asarray(original_pcd.points)
original_pcd_colors = np.asarray(original_pcd.colors) # the range is [0, 1] for each color
original_pcd_normals = np.asarray(original_pcd.normals)

all_points_tuples = [tuple(point.tolist()) for point in all_points]

for i in range(len(original_pcd_points)):
    point_tuple = tuple(original_pcd_points[i].tolist()) 
    if point_tuple not in all_points_tuples:
        all_points.append(original_pcd_points[i])
        all_colors.append((original_pcd_colors[i] * 255).astype(np.uint8))
        all_normals.append(original_pcd_normals[i])
        all_object_ids.append(-1)


all_points = np.vstack(all_points)
all_colors = np.vstack(all_colors)
all_normals = np.vstack(all_normals)
all_object_ids = np.vstack(all_object_ids)


# Transformation of the coordinates to have the alignment

transformed_points = copy.deepcopy(all_points)
if path_transformationMatrix:
    homogeneous_points = np.hstack((all_points, np.ones((all_points.shape[0], 1))))
    transformed_points_homogeneous = np.dot(homogeneous_points, transformation_matrix.T)
    transformed_points = transformed_points_homogeneous[:, :3]

# Build the ply file

combined_data = np.hstack((transformed_points, all_colors, all_normals, all_object_ids))

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
    f.write("property float nx\n")
    f.write("property float ny\n")
    f.write("property float nz\n")
    f.write("property int objectId\n")
    f.write("end_header\n")

    # Write point data
    for point in combined_data:
        f.write(f"{point[0]:.6f} {point[1]:.6f} {point[2]:.6f} {int(point[3])} {int(point[4])} {int(point[5])} {point[6]:.6f} {point[7]:.6f} {point[8]:.6f} {int(point[9])}\n")

colored_point_cloud = o3d.io.read_point_cloud(path_save_newPCD)
# o3d.visualization.draw_geometries([colored_point_cloud])


end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")



# TIMINGS:

# frl_apartment_0: 
# frl_apartment_1_to_frl_apartment_0: 
# frl_apartment_2_to_frl_apartment_0: 
# frl_apartment_3_to_frl_apartment_0: 
# frl_apartment_4_to_frl_apartment_0: 
# frl_apartment_5_to_frl_apartment_0: 
