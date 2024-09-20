'''Get the file colored_mesh_with_IDs.ply, i.e., the point cloud with a visible segmentation (given by the ground truth) of a scene from the Replica dataset
and create the file objects.json.
The header of a labels.instances.align.annotated.v2.ply from 3RScan appears like this:

ply
format ascii 1.0
element vertex 79398
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
property ushort objectId
property ushort globalId
property uchar NYU40
property uchar Eigen13
property uchar RIO27
element face 113403
property list uchar uint vertex_indices
end_header
-1.17901718616485596 -0.97001415491104126 1.13987147808074951 197 176 213 9 388 38 0 0
-1.16147065162658691 -1.0307769775390625 1.1398322582244873 197 176 213 9 388 38 0 0


and I want something similar for a .ply scene from Replica. For Replica, I will have something like:

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

Additionally, this script applies the transformation matrix so that there is an alignment between two Replica scenes.

'''

# TODO: as far as I remember there are things in the scenes that did not have a label. You may retrieve them and add them to the point clouds

import os
import random
import open3d as o3d
import numpy as np
import json

#
# Variables to change
#

path_meshSemantics = "/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/Segmentation" # folder containing the mesh_semantic.ply_i.ply
path_transformationMatrix = "/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/sgaligner_MOD_Replica/0GAIA/alignment_Replica/results_alignment/frl_apartment_1_to_frl_apartment_0/frl_apartment_1_to_frl_apartment_0.txt"
path_listInstances = "/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/list_instances.txt"
path_save_objectsJSON = "/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/SGAligner/objects.json"
usingTarget = True # False: the transformation will be applied, you are dealing with the source; True: you must not apply the transformation


#
# Associate a colour to each object
#

# Get the IDs of the objects (IDs are included in the filenames)
def extract_numbers_from_filenames(path_meshSemantics):
    numbers = []
    
    for filename in os.listdir(path_meshSemantics):
        if filename.startswith("mesh_semantic.ply_") and filename.endswith(".ply"):
            try:
                parts = filename.split('_')
                number_part = parts[-1].split('.')[0]  # get the 'i' part from 'mesh_semantic.ply_i.ply'
                number = int(number_part)  # convert to integer
                numbers.append(number)
            except ValueError:
                # If conversion to int fails, skip the file
                pass
    
    return sorted(numbers)

list_numbers = extract_numbers_from_filenames(path_meshSemantics)


# Create the dictionary that associates a color to an object
def create_colors_dict(list_numbers):
    random_dict = {}
    random.seed(1) # set the random colors
    
    for number in list_numbers:
        random_array = [random.randint(0, 255) for _ in range(3)]
        random_dict[number] = random_array
    
    return random_dict

random_dict = create_colors_dict(list_numbers)



#
# Put all the colored objects in a point cloud; the alignment has to be performed on the single instances.
# Save colored_mesh_with_IDs.ply 
#

# def load_and_color_point_clouds_segmentationOnly(path_meshSemantics, random_dict):
#     combined_point_clouds = []

#     for i in random_dict.keys():
#         filename = f'mesh_semantic.ply_{i}.ply'
#         filepath = os.path.join(path_meshSemantics, filename)
        
#         if os.path.exists(filepath):
#             pcd = o3d.io.read_point_cloud(filepath)
#             color = np.array(random_dict[i]) / 255.0  # normalize to range [0, 1] for Open3D
#             pcd.paint_uniform_color(color)
#             combined_point_clouds.append(pcd)

#     if combined_point_clouds:
#         full_point_cloud = combined_point_clouds[0]
#         for pcd in combined_point_clouds[1:]:
#             full_point_cloud += pcd
        
#         return full_point_cloud
#     else:
#         return None
    
transformation_matrix = np.loadtxt(path_transformationMatrix)

def get_data_for_pointCloud(path_meshSemantics, random_dict):
    all_points = []
    all_colors = []
    all_object_ids = []

    for i in random_dict.keys():
        filename = f'mesh_semantic.ply_{i}.ply'
        filepath = os.path.join(path_meshSemantics, filename)
        
        if os.path.exists(filepath):
            pcd = o3d.io.read_point_cloud(filepath)
            if not usingTarget:
                pcd.transform(transformation_matrix)
            points = np.asarray(pcd.points)

            color = np.array(random_dict[i])
            colors = np.tile(color, (points.shape[0], 1))

            object_id = np.full((points.shape[0], 1), i)

            all_points.append(points)
            all_colors.append(colors)
            all_object_ids.append(object_id)

    all_points = np.vstack(all_points)
    all_colors = np.vstack(all_colors)
    all_object_ids = np.vstack(all_object_ids)

    return all_points, all_colors, all_object_ids


points, colors, object_ids = get_data_for_pointCloud(path_meshSemantics, random_dict)
combined_data = np.hstack((points, colors, object_ids))

# Write the PLY file manually
output_ply = os.path.join(path_meshSemantics, "colored_mesh_with_IDs.ply")
with open(output_ply, 'w') as f:
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

colored_point_cloud = o3d.io.read_point_cloud(output_ply)
o3d.visualization.draw_geometries([colored_point_cloud])



#
# Create a dictionary containing id, label and ply_color.
# Save objects.json
#

obj_data = {"objects": []}

with open(path_listInstances, 'r') as file:
    for line in file:
        parts = line.split()

        obj_id = int(parts[0])
        label = parts[1]
        ply_color = random_dict[obj_id]
        ply_color_hex = '#{:02x}{:02x}{:02x}'.format(*ply_color) # format the ply_color as a hexadecimal string

        obj_data["objects"].append({
            "id": obj_id,
            "label": label,
            "ply_color": ply_color_hex
        })

# Save the dictionary to a JSON file
with open(path_save_objectsJSON, 'w') as json_file:
    json.dump(obj_data, json_file, indent=2)

