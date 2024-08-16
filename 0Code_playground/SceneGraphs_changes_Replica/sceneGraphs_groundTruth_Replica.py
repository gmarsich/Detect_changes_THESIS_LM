# environment: sceneGraphs_groundTruth_Replica

'''To retrieve the ground truth on the segmentation in a scene from the Replica dataset'''

from plyfile import PlyData, PlyElement
import numpy as np
import os
import open3d as o3d
import json
import pyviz3d.visualizer as viz

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

chosen_distance = distance_Euclidean_centerBoundingBoxes

threshold = 8 # threshold for the existance of an edge, in meters

path_pcd_scene_graph = os.path.join("/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_0/mesh.ply")

point_size = 15 # in the scene graph

distances_on = False # do you want the distances on the edges on the scene graph?



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
# Create list_info with information for each instance. Each element is in the form: [object_id, class_name, center]
#

path_info_semantic = os.path.join(path_in_base, name_semantic)

with open(path_info_semantic, 'r') as file:
    data = json.load(file)

objects = data.get('objects', [])
list_info = [] # remark that it will not be ordered

for obj in objects:
    obj_id = obj.get('id')
    class_name = obj.get('class_name')
    center = obj.get('oriented_bbox', {}).get('abb', {}).get('center', [])
    list_info.append([obj_id, class_name, center])


#TODO: be aware that we may have that `len(list_of_object_id_and_paths) != len(list_info)`, but I don't really know why. Some ids seem to be missing in the `.json` file



#
# Get the matrix with the distances between instances, and save it in matrix_distances_file.txt. Save also list_instances (without list_points_pcd) in list_objects.txt
#

list_instances, transposed_list_instances = get_list_instances(list_info, list_points)
matrix_distances = compute_distance_matrix(list_instances, compute_distance = chosen_distance)


'''

#
# Get the scene graph using PyViz3D
#

# I use the `PyViz3D` package (https://github.com/francisengelmann/PyViz3D),
    # taking inspiration from this example: https://github.com/francisengelmann/PyViz3D/blob/master/examples/example_point_clouds.py


def create_sceneGraph(list_instances, matrix_distances, threshold, custom_color=[0, 0, 0]):
    # custom_color gives the color for vertices and edges
    vertices = [label[2] for label in list_instances] # the vertices are the centers of the bounding boxes

    # Create lines for the edges and save the associated distances
    edges = []
    distances_str = []
    distances = []
    for i in range(len(matrix_distances)):
        for j in range(i + 1, len(matrix_distances[0])):
            if matrix_distances[i][j] <= threshold:
                    edges.append([i, j])
                    distances.append(matrix_distances[i][j])
                    distances_str.append(f"{matrix_distances[i][j]:.2f}")

    lines_start = np.array([vertices[i] for (i, j) in edges])
    lines_end = np.array([vertices[j] for (i, j) in edges])
    midpoints = (lines_start + lines_end) / 2

    lines_colors = np.array([custom_color for (i, j) in edges])

    return lines_start, lines_end, lines_colors, [np.array(row) for row in midpoints], distances, distances_str



v = viz.Visualizer()

pcd_scene_graph = o3d.io.read_point_cloud(path_pcd_scene_graph)

name = '3D segmentation'
point_positions = np.asarray(pcd_scene_graph.points)
point_colors = (np.asarray(pcd_scene_graph.colors) * 255).astype(np.uint8)

# Here we add point clouds to the visualiser
v.add_points(name, point_positions, point_colors, point_size=point_size, visible=False)

colors = [np.array([0, 0, 0]) for label in transposed_list_instances[0]] # TOSET

v.add_labels(name ='Labels',
                 labels = [label.upper() for label in transposed_list_instances[1]], # TOSET: if you want in capital letters or not
                 positions = transposed_list_instances[2],
                 colors = colors,
                 visible=True)

lines_start, lines_end, lines_colors, midpoints, _, distances_str = create_sceneGraph(list_instances, matrix_distances, threshold, custom_color=[0, 0, 0])

v.add_lines(name='Edges', lines_start=lines_start, lines_end=lines_end, colors=lines_colors, visible=True)

if distances_on:
    v.add_labels(name ='Distances',
                    labels = distances_str,
                    positions = midpoints,
                    colors = [0, 0, 0] * len(midpoints), # TOSET change the color of the text of distances
                    visible=True)

# When we added everything we need to the visualizer, we save it
v.save('sceneGraph_PyViz3D')


'''