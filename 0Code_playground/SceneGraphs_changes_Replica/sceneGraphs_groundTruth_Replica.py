# environment: sceneGraphs_groundTruth_Replica

'''To retrieve the ground truth on the segmentation in a scene from the Replica dataset'''

from plyfile import *
import numpy as np
import os
import open3d as o3d
import json
from scipy.spatial import KDTree
import csv
import pyviz3d.visualizer as viz

#
# Variables to set
#

path_in_base = '/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_0/habitat/'
name = "mesh_semantic.ply"
need_meshes = False # do you need the meshes of each instance of do you already have them?
path_to_output_ply = '/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_0/habitat/Segmentation/mesh_semantic.ply_47.ply' # instance to visualise as a test



#
# Get a folder containing a mesh in .ply format for each instance
#

if need_meshes:
    # Original inspiring code from: https://github.com/facebookresearch/Replica-Dataset/issues/17 . I 
    # begin of code

    path_in = os.path.join(path_in_base, name)

    print("Reading input...")
    file_in = PlyData.read(path_in)
    vertices_in = file_in.elements[0]
    faces_in = file_in.elements[1]

    print("Filtering data...")
    objects = {}
    for f in faces_in:
        object_id = f[1]
        if not object_id in objects:
            objects[object_id] = []
        objects[object_id].append((f[0],))

    print("Writing data...")
    segmentation_dir = os.path.join(path_in_base, "Segmentation/") # data will be saved in this folder
    os.makedirs(segmentation_dir, exist_ok=True)
    for object_id, faces in objects.items():
        path_out = segmentation_dir + name + f"_{object_id}.ply"
        faces_out = PlyElement.describe(np.array(faces, dtype=[('vertex_indices', 'O')]), 'face')
        PlyData([vertices_in, faces_out]).write(path_out) # vertices_in are the vertices of the entire scene; faces_out are the faces corresponding to the specific object ID

    # end of code



# #
# # If you want to visualise an instance, a mesh in the folder Segmentation
# #

# mesh = o3d.io.read_triangle_mesh(path_to_output_ply)

# if not mesh.has_triangles():
#     raise ValueError(f"Failed to load mesh from {path_to_output_ply}")

# mesh.compute_vertex_normals()

# # Visualize the mesh
# o3d.visualization.draw_geometries([mesh])



#
# Get the list list_file_paths with the paths of all the meshes (one mesh = one instance)
# Create list_points (each element is a list of points). Correspondence with list_file_paths
#

all_items = os.listdir(segmentation_dir)
list_file_paths = [os.path.join(segmentation_dir, item) for item in all_items if os.path.isfile(os.path.join(segmentation_dir, item))]
list_file_paths.sort(key=lambda x: int(x.split('_')[-1].split('.')[0])) # alphabetic order in the list_file_paths


