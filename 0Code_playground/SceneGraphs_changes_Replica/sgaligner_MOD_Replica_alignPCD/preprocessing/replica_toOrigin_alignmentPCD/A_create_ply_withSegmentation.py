'''MODIFIED TO GET ALL THE INSTANCE POINT CLOUDS (ONE POINT CLOUD FOR EACH INSTANCE) WITH THE CENTROID IN THE ORIGIN'''

'''Get the file colored_mesh_with_IDs_toOrigin.ply, i.e., the point cloud with a visible segmentation (given by the ground truth) of a scene from the Replica dataset
and create the file objects_toOrigin.json.
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


import os
import random
import open3d as o3d
import numpy as np
import json
import ast

#
# Variables to change
#

path_meshSemantics = "/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/Segmentation" # folder containing the mesh_semantic.ply_i.ply
path_transformationMatrix = "/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/sgaligner_MOD_Replica/0GAIA/alignment_Replica/results_alignment/frl_apartment_1_to_frl_apartment_0/frl_apartment_1_to_frl_apartment_0.txt"
path_listInstances = "/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/list_instances.txt"
path_save_objectsJSON = "/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/SGAligner_toOrigin/objects_toOrigin.json"
usingTarget = False # False: the transformation will be applied, you are dealing with the source; True: you must not apply the transformation



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
    used_colors = set()
    random.seed(1) # set the random colors
    
    for number in list_numbers:
        while True:
            random_array = tuple([random.randint(0, 255) for _ in range(3)])
            if random_array not in used_colors:
                used_colors.add(random_array)
                random_dict[number] = list(random_array)
                break
    
    return random_dict

random_dict = create_colors_dict(list_numbers)


# # OLD VERSION OF PREVIOUS CODE:
# def create_colors_dict(list_numbers):
#     random_dict = {}
#     random.seed(1) # set the random colors
    
#     for number in list_numbers:
#         random_array = [random.randint(0, 255) for _ in range(3)]
#         random_dict[number] = random_array
    
#     return random_dict



#
# Create a dictionary containing id, label and ply_color.
# Save objects_toOrigin.json
#

obj_data = {"objects": []}

with open(path_listInstances, 'r') as file:
    i = 0
    for line in file:
        parts = line.split('\t')

        obj_id = parts[0]
        label = parts[1]
        centroid_str = parts[2]
        centroid_ast = ast.literal_eval(centroid_str)
        centroid = list(centroid_ast)
        ply_color = random_dict[int(obj_id)]
        ply_color_hex = '#{:02x}{:02x}{:02x}'.format(*ply_color) # format the ply_color as a hexadecimal string

        obj_data["objects"].append({
            "count": i,
            "id": obj_id,
            "label": label,
            "original centroid": centroid, # be aware that some of the precision is lost from the .txt file
            "ply_color": ply_color_hex
        })

        i+=1

# Save the dictionary to a JSON file
with open(path_save_objectsJSON, 'w') as json_file:
    json.dump(obj_data, json_file, indent=2)



#
# Put all the colored objects in a point cloud, and each instance has its centroid in the origin; the alignment has to be performed on the single instances.
# Save colored_mesh_with_IDs_toOrigin.ply 
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


def apply_transformation_to_points(point, transformation_matrix):   
    # Convert the point to homogeneous coordinates (add 1 to make it [x, y, z, 1])
    point_homogeneous = np.append(point, 1)
    
    # Apply the transformation matrix (4x4) to the point
    transformed_point_homogeneous = np.dot(transformation_matrix, point_homogeneous)
    
    # Convert back to 3D coordinates by taking only the x, y, z components
    transformed_point = transformed_point_homogeneous[:3]
    
    return transformed_point


def get_data_for_pointCloud(path_meshSemantics, random_dict):
    all_points = []
    all_colors = []
    all_object_ids = []

    for i in random_dict.keys():
        filename = f'mesh_semantic.ply_{i}.ply'
        filepath = os.path.join(path_meshSemantics, filename)
        
        if os.path.exists(filepath):
            pcd = o3d.io.read_point_cloud(filepath)
            object_centroid = pcd.get_center()
            if not usingTarget:
                pcd.transform(transformation_matrix)
                object_centroid = pcd.get_center()

            transformation_matrix_toOrigin = np.identity(4)
            transformation_matrix_toOrigin[:3, 3] = -np.array(object_centroid)
            pcd.transform(transformation_matrix_toOrigin)

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
output_ply = os.path.join(path_meshSemantics, "colored_mesh_with_IDs_toOrigin.ply")
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



