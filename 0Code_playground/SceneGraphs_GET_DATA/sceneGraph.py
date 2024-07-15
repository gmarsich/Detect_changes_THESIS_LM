# environment: sceneGraphs_Gaia

import numpy as np
import os
import open3d as o3d
from scipy.spatial import distance
import copy
import pyviz3d.visualizer as viz
import numpy as np

import scannet200_constants # local file. From https://github.com/cvg/Mask3D/blob/e07b115fb7830d600f9db865489612f5739bbb50/mask3d/datasets/scannet200/scannet200_constants.py

pcd_mask3D = o3d.io.read_point_cloud(os.path.join("/local/home/gmarsich/data2TB/LabelMaker/processed_ARKitScenes/40753679/intermediate/scannet200_mask3d_1/mesh_labelled.ply")) # TODO TOSET: change the name of the point cloud to open
o3d.visualization.draw_geometries([pcd_mask3D])




# Path to "predictions.txt"
base_path = "/local/home/gmarsich/data2TB/LabelMaker/processed_ARKitScenes/40753679/intermediate/scannet200_mask3d_1" # TODO TOSET
path_predictions = os.path.join(base_path, "predictions.txt") # TODO TOSET: change if necessary

# Paths to the pred_mask files
path_pred_masks = os.path.join(base_path, "pred_mask") #TODO TOSET
all_files = os.listdir(path_pred_masks)
txt_files = [f for f in all_files if f.endswith('.txt')]

def extract_number(filename):
    return int(os.path.splitext(filename)[0])

txt_files.sort(key=extract_number)
sorted_txt_paths = [os.path.join(path_pred_masks, f) for f in txt_files]





def build_legend(path_predictions):
    with open(path_predictions, 'r') as file:
        lines = file.readlines()

    predictions = []

    for line in lines:
        parts = line.strip().split()
        filename = parts[0]
        file_number = filename.split('/')[1].split('.')[0]
        object_ID = int(parts[1])
        confidence = float(parts[2])

        predictions.append([file_number, object_ID, confidence])

    # Build a list with the info that I need
    objects = []

    for prediction in predictions:
        object_ID = prediction[1]
        
        # Find the object_ID in the objects list
        found = False
        for obj in objects:
            if obj[0] == object_ID:
                obj[1] += 1
                found = True
                break
        
        # If the object_ID was not found, add it to the list with a count of 1
        if not found:
            objects.append([object_ID, 1])


    #
    # Build a big table with the correspondences between VALID_CLASS_IDS_200, CLASS_LABELS_200 and SCANNET_COLOR_MAP_200 from scannet200_constants
    #

    table_scannet200 = []

    for class_id, label in zip(scannet200_constants.VALID_CLASS_IDS_200, scannet200_constants.CLASS_LABELS_200):
        color = scannet200_constants.SCANNET_COLOR_MAP_200[class_id]
        table_scannet200.append((class_id, label, color))

    # An alternative could be to get the colours from the point cloud and search for their assciated IDs (and name of the object) on
        # https://github.com/ScanNet/ScanNet/blob/master/BenchmarkScripts/ScanNet200/scannet200_constants.py


    #
    # Use the big table to add information to the list objects
    #

    # Add label and colour
    for obj in objects:
        object_ID = obj[0]
        
        for entry in table_scannet200:
            class_id, label, color = entry
            if object_ID == class_id:
                obj.append(label)
                obj.append(color)
                break

    # Sort the objects list by the ID (first element of each sublist)
    objects.sort(key=lambda x: x[0])
    return objects

objects = build_legend(path_predictions)





#
# Possible distance metrics
#

def distance_Euclidean_centroids(centroid_1, centroid_2):
    distance = np.linalg.norm(centroid_1 - centroid_2)
    return distance


def distance_Euclidean_closest_points(list_points_1, list_points_2):
    min_distance = np.inf
    for point1 in list_points_1:
        for point2 in list_points_2:
            dist = np.linalg.norm(point1 - point2)
            if dist < min_distance:
                min_distance = dist

    return min_distance


#
# Useful functions
#

def get_list_points(path_pred_mask, pcd_mask3D):
    points = np.asarray(pcd_mask3D.points)

    with open(path_pred_mask, 'r') as f:
        mask = np.array([int(line.strip()) for line in f])
    assert len(mask) == len(points)
    list_points = points[mask == 1]

    return list_points


def get_list_instances(path_predictions, sorted_txt_paths, pcd_mask3D):
    with open(path_predictions, 'r') as file:
        lines = file.readlines()

    list_instances = [] # will contain a list of [object_ID, label, position_centroid, color, list_points]

    for i, path_pred_mask in enumerate(sorted_txt_paths):
        parts = lines[i].strip().split()
        object_ID = int(parts[1])
        label = None

        list_points = get_list_points(path_pred_mask, pcd_mask3D)

        position_centroid = np.mean(list_points, axis=0)
        color = None  
        for index in range(len(objects)):
            if objects[index][0] == object_ID:
                label = objects[index][2]
                color = objects[index][3]
                #break
        list_instances.append([object_ID, label, position_centroid, color, list_points])

    transposed_list_instances = [list(row) for row in zip(*list_instances)]

    return list_instances, transposed_list_instances


def compute_distance_matrix(list_instances, compute_distance):
    matrix_distances = np.full((len(list_instances), len(list_instances)), np.inf)

    for i in range(len(matrix_distances)):
        for j in range(i + 1, len(matrix_distances[0])): # the matrix is symmetric

            if compute_distance == distance_Euclidean_centroids:
                matrix_distances[i][j] = compute_distance(list_instances[i][2], list_instances[j][2])
            else:
                matrix_distances[i][j] = compute_distance(list_instances[i][4], list_instances[j][4])
            
            matrix_distances[j][i] = matrix_distances[i][j]
    
    return matrix_distances




list_instances, transposed_list_instances = get_list_instances(path_predictions, sorted_txt_paths, pcd_mask3D)

matrix_distances = compute_distance_matrix(list_instances, compute_distance = distance_Euclidean_centroids) # TODO TOSET: change the distance metric you want to use






#
# COMPUTE THE SCENE GRAPH
#
# VERSION GAIA


threshold = 1.7 # TODO TOSET: distance threshold in meters


# Function to create the graph with colors
def create_sceneGraph(list_instances, matrix_distances, color_lines, ceiling_represented=False): # max value of color_lines is [255, 255, 255]; ceiling_represented indicates if the wall will appear in the scene graph or not
    index_ceiling = np.inf
    if not ceiling_represented:
        for i in range(len(list_instances)):
            if 41 == list_instances[i][0]:
                index_ceiling = i

    vertices = [label[2] for label in list_instances] # the vertices are the centroids of the instances

    colors = [np.array(label[3]) / 255.0 for label in list_instances]

    if not ceiling_represented:
        del vertices[index_ceiling]
        del colors[index_ceiling]
    
    # Create a point cloud for the vertices
    points = o3d.geometry.PointCloud()
    points.points = o3d.utility.Vector3dVector(vertices)
    points.colors = o3d.utility.Vector3dVector(colors)

    # Update the matrix_distances to be used, in case
    matrix_distances_copy = copy.deepcopy(matrix_distances)
    if not ceiling_represented:
        matrix_distances_copy = np.delete(matrix_distances_copy, index_ceiling, axis=0)
        matrix_distances_copy = np.delete(matrix_distances_copy, index_ceiling, axis=1)

    edges = []
    for i in range(len(matrix_distances_copy)):
        for j in range(i + 1, len(matrix_distances_copy[0])):
            if matrix_distances_copy[i][j] <= threshold:
                    edges.append([i, j])
    
    lines = o3d.geometry.LineSet()
    lines.points = o3d.utility.Vector3dVector(vertices)
    lines.lines = o3d.utility.Vector2iVector(edges)
    lines.paint_uniform_color(color_lines)

    return points, lines


# Function for visualisation
def visualise_sceneGraph(points, lines, point_size=15, line_width=4):
    # Create a visualization window and set point size
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(points)
    vis.add_geometry(lines)

    # Set point and line size
    render_option = vis.get_render_option()
    render_option.point_size = point_size

    vis.get_view_control().convert_to_pinhole_camera_parameters()
    vis.get_render_option().line_width = line_width

    # Run the visualization
    vis.run()
    vis.destroy_window()


points, lines = create_sceneGraph(list_instances, matrix_distances, color_lines=[0, 0, 0])

# visualise_sceneGraph(points, lines, point_size=10) # uncomment if you want to see the scene graph (no saving of the data)


def save_sceneGraph(points, lines, vertices_filename="sceneGraph_vertices.ply", edges_filename="sceneGraph_edges.ply"):
    # Create the "sceneGraph" directory if it doesn't exist
    if not os.path.exists("sceneGraph_Gaia"):
        os.makedirs("sceneGraph_Gaia")

    # Save the point cloud and line set to the "sceneGraph" directory
    vertices_filepath = os.path.join("sceneGraph_Gaia", vertices_filename)
    edges_filepath = os.path.join("sceneGraph_Gaia", edges_filename)
    o3d.io.write_point_cloud(vertices_filepath, points)
    o3d.io.write_line_set(edges_filepath, lines)


def load_and_visualise_sceneGraph(vertices_filename="sceneGraph_vertices.ply", edges_filename="sceneGraph_edges.ply", point_size=15, line_width=4):
    # Load the point cloud and line set
    point_cloud_filepath = os.path.join("sceneGraph_Gaia", vertices_filename)
    line_set_filepath = os.path.join("sceneGraph_Gaia", edges_filename)
    points = o3d.io.read_point_cloud(point_cloud_filepath)
    lines = o3d.io.read_line_set(line_set_filepath)

    # Create a visualization window and set point size
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(points)
    vis.add_geometry(lines)

    # Set point and line size
    render_option = vis.get_render_option()
    render_option.point_size = point_size
    
    vis.get_view_control().convert_to_pinhole_camera_parameters()
    vis.get_render_option().line_width = line_width

    # Run the visualization
    vis.run()
    vis.destroy_window()


save_sceneGraph(points, lines)

load_and_visualise_sceneGraph()



# VERSION PYVIZ3D

threshold = 1.7 # TODO TOSET: distance threshold in meters

def create_sceneGraph(list_instances, matrix_distances, threshold, ceiling_represented=False, default_color_on=True, custom_color=[0, 0, 0]):
    # default_color_on=True will color the edges with some colors of the vertices that the edge connects. If it is False, choose a color with custom_color for all the edges
    index_ceiling = np.inf
    if not ceiling_represented:
        for i in range(len(list_instances)):
            if 41 == list_instances[i][0]:
                index_ceiling = i

    vertices = [label[2] for label in list_instances] # the vertices are the centroids of the instances

    colors = [np.array(label[3]) for label in list_instances]

    if not ceiling_represented:
        del vertices[index_ceiling]
        del colors[index_ceiling]

    # Update the matrix_distances to be used, in case
    matrix_distances_copy = copy.deepcopy(matrix_distances)
    if not ceiling_represented:
        matrix_distances_copy = np.delete(matrix_distances_copy, index_ceiling, axis=0)
        matrix_distances_copy = np.delete(matrix_distances_copy, index_ceiling, axis=1)

    # Create lines for the edges and save the associated distances
    edges = []
    distances_str = []
    distances = []
    for i in range(len(matrix_distances_copy)):
        for j in range(i + 1, len(matrix_distances_copy[0])):
            if matrix_distances_copy[i][j] <= threshold:
                    edges.append([i, j])
                    distances.append(matrix_distances[i][j])
                    distances_str.append(f"{matrix_distances[i][j]:.2f}")

    lines_start = np.array([vertices[i] for (i, j) in edges])
    lines_end = np.array([vertices[j] for (i, j) in edges])
    midpoints = (lines_start + lines_end) / 2

    if default_color_on:
        lines_colors = np.array([colors[i] for (i, j) in edges]) # the color of the edge is given by the first vertex
    else:
        lines_colors = np.array([custom_color for (i, j) in edges])

    return lines_start, lines_end, lines_colors, [np.array(row) for row in midpoints], distances, distances_str



v = viz.Visualizer()

name = '3D segmentation'
point_positions = np.asarray(pcd_mask3D.points)
point_colors = (np.asarray(pcd_mask3D.colors) * 255).astype(np.uint8)
point_size = 15 # TODO TOSET

# Here we add point clouds to the visualiser
v.add_points(name, point_positions, point_colors, point_size=point_size, visible=False)

v.add_labels(name ='Labels',
                 labels = [label.upper() for label in transposed_list_instances[1]], # TODO TOSET: if you want in capital letters or not
                 positions = transposed_list_instances[2],
                 colors = transposed_list_instances[3],
                 visible=True)

lines_start, lines_end, lines_colors, midpoints, _, distances_str = create_sceneGraph(list_instances, matrix_distances, threshold, ceiling_represented=False, default_color_on=True, custom_color=[0, 0, 0])

v.add_lines(name='Edges', lines_start=lines_start, lines_end=lines_end, colors=lines_colors, visible=True)

# The following is to have the distances among instances
distances_on = True #TODO TOSET
if distances_on:
    v.add_labels(name ='Distances',
                    labels = distances_str,
                    positions = midpoints,
                    colors = [0, 0, 0] * len(midpoints), # TODO TOSET change the color of the text of distances
                    visible=True)

# When we added everything we need to the visualizer, we save it.
v.save('sceneGraph_PyViz3D')

