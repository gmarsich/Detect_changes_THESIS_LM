# environment: sceneGraphs_groundTruth_Replica

'''To retrieve the ground truth on the segmentation in a scene from the Replica dataset.
This code uses matrix_distances_file.txt (in the filename the distance that has been used is specified) and list_objects.txt to create a scene graph.'''

import pyviz3d.visualizer as viz
import os
import numpy as np
import open3d as o3d


#
# Variables to set
#

path_to_matrixDistance = '/local/home/gmarsich/Desktop/Thesis/matrix_distances_file<function distance_Euclidean_centerBoundingBoxes at 0x7f55480b1750>.txt'
path_to_listObjects = '/local/home/gmarsich/Desktop/Thesis/list_objects.txt'

list_things = [0, 1, 2, 3, 4, 5] # which objects do you want to take into account? Numbers indicate the object_id

threshold = 8 # threshold for the existance of an edge, in meters

path_pcd_scene_graph = os.path.join("/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_1/mesh.ply")

point_size = 15 # in the scene graph

distances_on = False # do you want the distances on the edges in the scene graph?



#
# Collect the data from the .txt files and define a function to get the useful things for PyViz3D
#

# I use the `PyViz3D` package (https://github.com/francisengelmann/PyViz3D),
    # taking inspiration from this example: https://github.com/francisengelmann/PyViz3D/blob/master/examples/example_point_clouds.py

with open(path_to_matrixDistance, 'r') as file:
    next(file) # skip the first line
    matrix_distances = np.loadtxt(file)


list_objects = []

with open(path_to_listObjects, 'r') as file:
    for line in file:
        parts = line.strip().split('\t')

        obj_id = int(parts[0])
        class_name = parts[1]
        center = list(map(float, parts[2].split(', ')))

        list_objects.append([obj_id, class_name, center])

transposed_list_objects = [list(row) for row in zip(*list_objects)]


def create_sceneGraph(list_objects, matrix_distances, threshold, custom_color=[0, 0, 0]):
    # custom_color gives the color for vertices and edges
    vertices = [label[2] for label in list_objects] # the vertices are the centers of the bounding boxes

    # Create lines for the edges and save the associated distances
    edges = []
    distances = []
    distances_str = []
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

colors = [np.array([0, 0, 0]) for label in transposed_list_objects[0]] # TOSET

v.add_labels(name ='Labels',
                 labels = [label.upper() for label in transposed_list_objects[1]], # TOSET: if you want in capital letters or not
                 positions = transposed_list_objects[2],
                 colors = colors,
                 visible=True)

lines_start, lines_end, lines_colors, midpoints, _, distances_str = create_sceneGraph(list_objects, matrix_distances, threshold, custom_color=[0, 0, 0])

#v.add_lines(name='Edges', lines_start=lines_start, lines_end=lines_end, colors=lines_colors, visible=True)

if distances_on:
    v.add_labels(name ='Distances',
                    labels = distances_str,
                    positions = midpoints,
                    colors = [0, 0, 0] * len(midpoints), # TOSET change the color of the text of distances
                    visible=True)

# When we added everything we need to the visualizer, we save it
v.save('sceneGraph_PyViz3D')


