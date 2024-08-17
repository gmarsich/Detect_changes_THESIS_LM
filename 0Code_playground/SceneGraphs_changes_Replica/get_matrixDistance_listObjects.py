# environment: sceneGraphs_groundTruth_Replica

'''To retrieve the ground truth on the segmentation in a scene from the Replica dataset.
This code creates two files, matrix_distances_file.txt (in the filename the distance that has been used is specified) and list_objects.txt.
They will be used later to get the scene graph.'''

from plyfile import PlyData, PlyElement
import numpy as np
import os
import open3d as o3d
import json

from side_code.side_code import * # local file


#
# Variables to set
#

path_in_base = '/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_0/habitat/'
name = "mesh_semantic.ply"

segmentation_dir = os.path.join(path_in_base, "Segmentation/")  # data of instance point clouds will be / are saved in this folder

need_pcd_instances = False # do you need to generate the point cloud of each instance or do you already have them?
path_to_output_ply = '/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_0/habitat/Segmentation/mesh_semantic.ply_47.ply' # instance to visualise as a test

name_semantic = "info_semantic.json"

chosen_distance = distance_Euclidean_centroids



#
# Get a folder containing for each instance a point cloud (storing also the faces) in .ply format
#

if need_pcd_instances:
    # Original inspiring code from: https://github.com/facebookresearch/Replica-Dataset/issues/17

    path_in = os.path.join(path_in_base, name)

    print("Reading input...")
    file_in = PlyData.read(path_in)
    vertices_in = np.array(file_in.elements[0].data)  # convert to numpy array for easier manipulation
    faces_in = np.array(file_in.elements[1].data)

    print("Filtering data...")
    objects = {}
    for f in faces_in:
        object_id = f[1]
        if object_id not in objects:
            objects[object_id] = {'faces': [], 'vertex_indices': set()}
        objects[object_id]['faces'].append(f[0])  # faces will basically be a list of faces (each face is associated to its vertexes)
        objects[object_id]['vertex_indices'].update(f[0])  # vertex_indices will be a set of vertexes

    print("Writing data...")
    os.makedirs(segmentation_dir, exist_ok=True)
    for object_id, data in objects.items():
        relevant_vertices = np.array([vertices_in[i] for i in data['vertex_indices']], dtype=vertices_in.dtype)

        # Create a mapping from old vertex indices to new ones
        old_to_new_index = {old_idx: new_idx for new_idx, old_idx in enumerate(sorted(data['vertex_indices']))}

        # Reindex the faces directly into a list of tuples
        reindexed_faces = [(tuple(old_to_new_index[idx] for idx in face),) for face in data['faces']]

        # Convert to PlyElement
        vertices_out = PlyElement.describe(relevant_vertices, 'vertex')
        faces_out = PlyElement.describe(np.array(reindexed_faces, dtype=[('vertex_indices', 'i4', (len(data['faces'][0]),))]), 'face')

        # Write out the ply file for this object
        path_out = os.path.join(segmentation_dir, f"{name}_{object_id}.ply")
        PlyData([vertices_out, faces_out]).write(path_out)



# #
# # If you want to visualise an instance, a point cloud in the folder Segmentation
# #

# pcd_test = o3d.io.read_point_cloud(path_to_output_ply)
# o3d.visualization.draw_geometries([pcd_test])



#
# Get the list list_of_object_id_and_paths made of lists in the form [object_id, path] of all the point clouds (one point cloud = one instance = one [object_id, path])
# Create list_points, made of lists in the form [object_id, list_points_pcd]
#

all_items = os.listdir(segmentation_dir)
list_file_paths = [os.path.join(segmentation_dir, item) for item in all_items if os.path.isfile(os.path.join(segmentation_dir, item))]

list_of_object_id_and_paths = []
for path in list_file_paths:
    basename = os.path.basename(path)
    try:
        object_id_str = basename.split('_')[-1].split('.')[0]
        object_id = int(object_id_str)
        list_of_object_id_and_paths.append([object_id, path])
    except ValueError:
        print(f"Error processing file: {basename}")

list_of_object_id_and_paths.sort(key=lambda x: x[0])

list_points = []

for l in list_of_object_id_and_paths:
    pcd = o3d.io.read_point_cloud(l[1])
    list_points.append([l[0], np.asarray(pcd.points)])



#
# Create list_labels with labels for each instance. Each element is in the form: [object_id, class_name]
#

path_info_semantic = os.path.join(path_in_base, name_semantic)

with open(path_info_semantic, 'r') as file:
    data = json.load(file)

objects = data.get('objects', [])
list_labels = [] # remark that it will not be ordered

for obj in objects:
    obj_id = obj.get('id')
    class_name = obj.get('class_name')
    list_labels.append([obj_id, class_name])


#TODO: be aware that we may have that `len(list_of_object_id_and_paths) != len(list_labels)`, but I don't really know why. Some ids seem to be missing in the `.json` file



#
# Get the matrix with the distances between instances, and save it in matrix_distances_file.txt (in the filename the distance that has been used is specified). Save also list_instances in list_objects.txt
#

list_instances = get_list_instances(list_labels, list_points) # list with elements in the form [obj_id, class_name, centroid, points]
matrix_distances = compute_distance_matrix(list_instances, compute_distance = chosen_distance)
