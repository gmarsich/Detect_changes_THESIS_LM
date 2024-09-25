'''Get the file colored_mesh.ply, i.e., the point cloud with a visible segmentation of a scene from the Replica dataset'''

import os
import random
import open3d as o3d
import numpy as np

#
# Variables to change
#

path_meshSemantics = "/local/home/gmarsich/Desktop/data_Replica/frl_3/Segmentation" # folder containing the mesh_semantic.ply_i.ply



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
# Put all the colored objects in a point cloud
#

def load_and_color_point_clouds(path_meshSemantics, random_dict):
    combined_point_clouds = []

    for i in random_dict.keys():
        filename = f'mesh_semantic.ply_{i}.ply'
        filepath = os.path.join(path_meshSemantics, filename)
        
        if os.path.exists(filepath):
            pcd = o3d.io.read_point_cloud(filepath)
            color = np.array(random_dict[i]) / 255.0  # normalize to range [0, 1] for Open3D
            pcd.paint_uniform_color(color)
            combined_point_clouds.append(pcd)

    if combined_point_clouds:
        full_point_cloud = combined_point_clouds[0]
        for pcd in combined_point_clouds[1:]:
            full_point_cloud += pcd
        
        return full_point_cloud
    else:
        return None

colored_point_cloud = load_and_color_point_clouds(path_meshSemantics, random_dict)
o3d.visualization.draw_geometries([colored_point_cloud])
#o3d.io.write_point_cloud(os.path.join(path_meshSemantics, "colored_mesh.ply"), colored_point_cloud)