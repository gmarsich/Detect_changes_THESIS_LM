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

path_to_matrixDistance = '/local/home/gmarsich/Desktop/data_Replica/matrix_distances_file_distance_Euclidean_centroids_frl_0.txt'
path_to_listObjects = '/local/home/gmarsich/Desktop/data_Replica/list_objects_frl_0.txt'

# list_things = [0, 1, 2, 3, 4, 5] # which objects do you want to take into account? Numbers indicate the object_id # TODO: a possible improvement in the code

threshold = 1 # threshold for the existance of an edge, in meters

path_pcd_scene_graph = os.path.join("/local/home/gmarsich/data2TB/DATASETS/Replica/frl_apartment_0/mesh.ply") # path to the original point cloud

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
        centroid_str = parts[2].strip('()')  # remove the parentheses around the centroid
        centroid = list(map(float, centroid_str.split(', ')))

        points_str = parts[3]
        points = [np.array(list(map(float, point.split(', ')))) for point in points_str.split('; ')]

        list_objects.append([obj_id, class_name, centroid, points])

transposed_list_objects = [list(row) for row in zip(*list_objects)]


def create_sceneGraph(list_objects, matrix_distances, threshold, custom_color=[0, 0, 0]):
    # custom_color gives the color for vertices and edges
    vertices = [label[2] for label in list_objects] # the vertices are the centroids

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



#
# Get a array_allPoints with all the points, associate colors to instances creating a list list_colors
#

np.random.seed(42)

list_allPoints_tmp = []
for obj_id, class_name, centroid, points in list_objects:
    list_allPoints_tmp.extend(points)
array_allPoints = np.asarray(list_allPoints_tmp)

list_colors = (np.random.rand(len(list_objects), 3) * 255).astype(np.uint8) # each element describes the color for an instace
array_colors = []
for i in range(len(list_objects)):
    array_colors.extend([list_colors[i]] * len(list_objects[i][3]))
array_colors = np.asarray(array_colors).astype(np.uint8) # contains the colors for each point



#
# Generate the rendering of the ground truth segmentation and the scene graph
#

v = viz.Visualizer()

# Original point cloud
pcd_scene_graph = o3d.io.read_point_cloud(path_pcd_scene_graph)
point_positions = np.asarray(pcd_scene_graph.points)
point_colors = (np.asarray(pcd_scene_graph.colors) * 255).astype(np.uint8)
v.add_points('Point cloud', point_positions, point_colors, point_size=point_size, visible=False)

# Ground truth segmentation
v.add_points('Segmentation', array_allPoints, array_colors, point_size=point_size, visible=False)

# Labels for the scene graph
colors = list_colors
v.add_labels(name ='Labels',
                 labels = [label.upper() for label in transposed_list_objects[1]], # TOSET: if you want in capital letters or not
                 positions = transposed_list_objects[2],
                 colors = colors,
                 visible=True)

# Edges of the scene graph
lines_start, lines_end, lines_colors, midpoints, _, distances_str = create_sceneGraph(list_objects, matrix_distances, threshold, custom_color=[0, 0, 0])
v.add_lines(name='Edges', lines_start=lines_start, lines_end=lines_end, colors=lines_colors, visible=True)

# Distances on the scene graph
if distances_on:
    v.add_labels(name ='Distances',
                    labels = distances_str,
                    positions = midpoints,
                    colors = [0, 0, 0] * len(midpoints), # TOSET change the color of the text of distances
                    visible=True)

# Save the rendering
v.save('sceneGraph_PyViz3D')
