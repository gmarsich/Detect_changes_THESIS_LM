''' Class SceneGraph: given as input a .ply with this header:
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

builds the SceneGraph object.

Since I specifically deal with Replica dataset, and in particular with the frl apartments some preprocessing was performed to get the things in a way I liked.

Other things that can be used to enrich the scene graph:

- path_distanceMatrix
- path_associationsObjectIdIndex
- path_listInstances
- path_colorDict_frlApartments

'''

import numpy as np
import open3d as o3d
import random
import json
from datetime import datetime
import os
import copy
import pyviz3d.visualizer as Visualiser


# side function
def create_colors_dict(list_numbers):
    random_dict = {}
    used_colors = set()
    random.seed(1) # set the random colors
    
    for number in list_numbers:
        while True:
            random_array = tuple([random.randint(0, 255) for _ in range(3)])
            if random_array not in used_colors:
                used_colors.add(random_array)
                random_dict[str(number)] = list(random_array)
                break
    
    return random_dict


# side function
def create_cylinder_between_points(point1, point2, color, radius=0.02):

    point1 = np.array(point1)
    point2 = np.array(point2)
    
    # Create cylinder geometry
    height = np.linalg.norm(point2 - point1)
    cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius=radius, height=height)
    
    mid_point = (point1 + point2) / 2

    direction = (point2 - point1) / height  # compute the direction from point1 to point2
    
    # Create a rotation matrix that aligns the cylinder's z-axis to the direction vector
    z_axis = np.array([0, 0, 1])  # default axis of the cylinder
    axis = np.cross(z_axis, direction)  # axis of rotation
    angle = np.arccos(np.dot(z_axis, direction))  # angle of rotation
    
    # Handle cases where the direction is aligned with the z-axis
    if np.linalg.norm(axis) > 1e-6:  # if the axis is non-zero
        axis = axis / np.linalg.norm(axis)  # normalize the rotation axis
        rotation_matrix = o3d.geometry.TriangleMesh.get_rotation_matrix_from_axis_angle(axis * angle)
        cylinder.rotate(rotation_matrix)
    
    cylinder.translate(mid_point) # translate the cylinder to the mid-point between the two points

    cylinder.paint_uniform_color(color) # set the color of the cylinder
    
    return cylinder


# side function
def create_sphere_at_point(point, color, radius = 0.1):
    sphere = o3d.geometry.TriangleMesh.create_sphere(radius)
    sphere.translate(point)  # move the sphere to the specified point
    sphere.paint_uniform_color(color)
    return sphere




class SceneGraph(): # possible attributes: self.complete_pointCloud, self.nodes, self.matrix_distances, self.associations_objectIdIndex
    # OK
    def __init__(self):
        self.nodes = {}

    # OK
    def populate_SceneGraph(self, path_plyFile, path_distanceMatrix = None, path_associationsObjectIdIndex = None, path_listInstances = None, path_colorDict_frlApartments = None):
        # path_distanceMatrix: if matrixDistances.txt (together with associations_objectIdIndex.json) is provided, the attribute self.matrix_distances (that is the matrix with distances) will be added
        # path_associationsObjectIdIndex: if associations_objectIdIndex.json (together with matrixDistances.txt) is provided, the attribute self.associations_objectIdIndex (given an objectID, which is the its index in self.matrix_distances?) is added
        # path_listInstances: if list_instances.txt is provided, the node will also contain the label of the instance
        # path_colorDict_frlApartments: if colorDict_frlApartments.json is provided, the node will also contain the specific color associated to that label
        
        self.complete_pointCloud = o3d.io.read_point_cloud(path_plyFile)

        with open(path_plyFile, 'r') as file:
            lines = file.readlines()

        start_idx = 0

        for i, line in enumerate(lines):
            if line.strip() == "end_header":
                start_idx = i + 1
                break
        
        for line in lines[start_idx:]:
            components = line.split()

            x, y, z = map(float, components[:3])
            red, green, blue = map(int, components[3:6])
            nx, ny, nz = map(float, components[6:9])
            objectId = components[9]

            if objectId not in self.nodes.keys():
                self.nodes[objectId] = {
                    'points_geometric': [],
                    'points_color': [],
                    'points_normals': [],
                    'centroid': None
                    }
            
            self.nodes[objectId]['points_geometric'].append([x, y, z])
            self.nodes[objectId]['points_color'].append([red, green, blue])
            self.nodes[objectId]['points_normals'].append([nx, ny, nz])
        
        for objectId, data in self.nodes.items():
            points_geometric = np.array(data['points_geometric'])
            centroid = list(np.mean(points_geometric, axis=0))
            self.nodes[objectId]['centroid'] = centroid

        # # Convert lists to numpy arrays
        # for objectId, data in self.nodes.items():
        #     self.nodes[objectId]['points_geometric'] = np.array(data['points_geometric'])
        #     self.nodes[objectId]['points_color'] = np.array(data['points_color'])
        #     self.nodes[objectId]['points_normals'] = np.array(data['points_normals'])


        # Add a color for the segmentation

        list_numbers = list(self.nodes.keys())
        color_dict = create_colors_dict(list_numbers)

        for objectId in self.nodes:
            self.nodes[objectId]['ply_color'] = color_dict[objectId]



        # If path_distanceMatrix and path_associationsObjectIdIndex are not None save the distances in a matrix
        
        if path_distanceMatrix and path_associationsObjectIdIndex:
            matrix = []
            with open(path_distanceMatrix, 'r') as file:
                next(file)  # SKIP THE FIRST LINE OF THE FILE. In my files, the first line is blank
                for line in file:
                    row = line.strip().split()
                    matrix.append([float(element) for element in row])

            self.matrix_distances = matrix

            with open(path_associationsObjectIdIndex, 'r') as json_file:
                self.associations_objectIdIndex = json.load(json_file)



        # If path_listInstances is not None, associate the labels

        if path_listInstances:
            
            labels = {}

            with open(path_listInstances, 'r') as file:
                for line in file:
                    parts = line.strip().split() # split the line by tab or whitespace

                    objectId = parts[0]
                    label = parts[1]

                    labels[objectId] = label

            for objectId, data in self.nodes.items():
                if objectId in labels:
                    data['label'] = labels[objectId]
                else:
                    data['label'] = 'None'


        # If path_colorDict_frlApartments is not None, associate the specific color to each label.
        # Be aware that you also need path_listInstances!

        if path_colorDict_frlApartments and path_listInstances:
            with open(path_colorDict_frlApartments, 'r') as json_file:
                data_dict = json.load(json_file)

            for objectId, data in self.nodes.items():
                label = data['label']
                data['absolute color'] = data_dict.get(label, [0, 0, 0]) # if the label does not exist in the dictionary (in my case, I will have "None", the color will be black)
                self.nodes[objectId]['absolute color'] = data['absolute color']
    
    # OK
    def load_SceneGraph(self, path_SceneGraph_folder): # CAVEAT: the complete point cloud is saved differently from the one that is loaded with populate_SceneGraph

        path_pcd_complete = os.path.join(path_SceneGraph_folder, 'pcd.ply')
        self.complete_pointCloud = o3d.io.read_point_cloud(path_pcd_complete)

        path_nodes = os.path.join(path_SceneGraph_folder, 'nodes.json')
        with open(path_nodes, 'r') as json_file: # populate self.nodes
            self.nodes = json.load(json_file)


        path_matrixDistances = os.path.join(path_SceneGraph_folder, 'matrix_distances.txt')
        if os.path.exists(path_matrixDistances):
            matrix = []
            with open(path_matrixDistances, 'r') as file: # populate self.matrix_distances
                next(file) # SKIP THE FIRST LINE OF THE FILE. In my files, the first line is blank
                for line in file:
                    row = line.strip().split()
                    matrix.append([float(element) for element in row])

            self.matrix_distances = matrix

            path_associationsObjectIdIndex = os.path.join(path_SceneGraph_folder, 'associations_objectIdIndex.json')
            with open(path_associationsObjectIdIndex, 'r') as json_file: # populate self.associations_objectIdIndex
                self.associations_objectIdIndex = json.load(json_file)
        
        return

    # OK
    def print_info_node(self, objectId):
        print(self.nodes[objectId])

    # OK
    def get_pointCloud(self, objectId, wantVisualisation = False):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(np.array(self.nodes[objectId]['points_geometric']))
        pcd.colors = o3d.utility.Vector3dVector(np.array(self.nodes[objectId]['points_color']) / 255) # normalise from range 0-255 to range 0-1
        pcd.normals = o3d.utility.Vector3dVector(np.array(self.nodes[objectId]['points_normals']))
        
        if wantVisualisation:
            o3d.visualization.draw_geometries([pcd])

        return pcd
    
    # OK
    def save_SceneGraph(self):
        # Create the folder where to store the data. Same folder of where this very same script is

        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        folder_name = f'sceneGraph_{current_time}'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(current_dir, folder_name)
        os.makedirs(folder_path)

        # Save the data in the folder

        o3d.io.write_point_cloud(os.path.join(folder_path, 'pcd.ply'), self.complete_pointCloud)
        
        with open(os.path.join(folder_path, 'nodes.json'), 'w') as json_file: # save self.nodes
            json.dump(self.nodes, json_file, indent=4)

        if self.matrix_distances:
            with open(os.path.join(folder_path, 'matrix_distances.txt'), 'w') as text_file: # save self.matrix_distances if it exists
                text_file.write('\n') # FIRST LINE HAS TO BE BLANK to be coherent with the files I had generated before
                for row in self.matrix_distances:
                    text_file.write(' '.join(map(str, row)) + '\n')

        if self.associations_objectIdIndex:
            with open(os.path.join(folder_path, 'associations_objectIdIndex.json'), 'w') as json_file: # save self.associations_objectIdIndex if it exists
                json.dump(self.associations_objectIdIndex, json_file, indent=4)

        # Write a message to reassure the user

        print(f'The files composing the scene graphs were saved to: {folder_path}') 

        return
    
    # OK (maybe check withUpdates)
    def get_visualisation_SceneGraph(self, list_IDs, threshold, color = 'absoluteColor'):
        # color: 'withUpdates' (show how the objects changed), 'randomColor' (given by self.nodes[objectId]['ply_color']), 'absoluteColor' (given by self.nodes[objectId]['absolute color'])

        # Get the vertices and the point clouds

        list_vertices = []
        list_centroids = []
        list_colors_vertices = []
        list_labels = []
        PCDs = []
        for objectId in list_IDs:

            positions_vertex = self.nodes[str(objectId)]['centroid'] # the vertices are the centroids of the instances
            list_labels.append(str(objectId) + " (" + self.nodes[str(objectId)]['label'] + ")")
            
            if color == 'absoluteColor':
                color_vertex = np.array(self.nodes[str(objectId)]['absolute color']) / 255
            if color == 'withUpdates':
                color_vertex = np.array(self.nodes[str(objectId)]['color update']) / 255
            if color == 'randomColor':
                color_vertex = np.array(self.nodes[str(objectId)]['ply_color']) / 255
            
            sphere = create_sphere_at_point(positions_vertex, color_vertex)
            list_centroids.append(positions_vertex)
            list_colors_vertices.append(color_vertex)
            list_vertices.append(sphere)

            pcd_instance = o3d.geometry.PointCloud()
            pcd_instance.points = o3d.utility.Vector3dVector(np.array(self.nodes[str(objectId)]['points_geometric']))
            list_colors = [color_vertex for index in range(len(pcd_instance.points))]
            pcd_instance.colors = o3d.utility.Vector3dVector(np.array(list_colors))
            PCDs.append(pcd_instance)


        # Get the edges

        list_edges = []
        list_pairs_edges = []
        for i in range(len(list_IDs)):
            for j in range(i + 1, len(list_IDs)):
                objectID_to_index_i = int(self.associations_objectIdIndex[str(list_IDs[i])])
                objectID_to_index_j = int(self.associations_objectIdIndex[str(list_IDs[j])])

                if self.matrix_distances[objectID_to_index_i][objectID_to_index_j] <= threshold:
                    centroid_i = self.nodes[str(list_IDs[i])]['centroid']
                    centroid_j = self.nodes[str(list_IDs[j])]['centroid']
                    list_pairs_edges.append([centroid_i, centroid_j])
                    current_edge = create_cylinder_between_points(centroid_i, centroid_j, color = np.array([0, 0, 0]) / 255) # TOSET you can set a different color for the edges
                    list_edges.append(current_edge)


        return list_vertices, list_centroids, list_colors_vertices, list_labels, PCDs, list_edges, list_pairs_edges

    # OK
    def draw_SceneGraph_PyViz3D(self, list_centroids, list_colors_vertices, list_labels, list_pairs_edges, PCDs, wantLabels = True):

        # Functions to adjust the origin of the axis

        def centering_axes(points): # by Joana
            point_cloud_centroid = np.mean(points, axis=0)
            points = points - point_cloud_centroid
            return points, point_cloud_centroid
        
        def transform_points(points, point_cloud_centroid): # by Joana
            return points - point_cloud_centroid
        
        
        # Folder to save the results

        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        folder_name = f'sceneGraph_PyViz3D_{current_time}'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(current_dir, folder_name)


        # Build the rendering of the points

        v = Visualiser.Visualizer()

        point_positions, centroid = centering_axes(np.asarray(self.complete_pointCloud.points))
        point_colors = (np.asarray(self.complete_pointCloud.colors) * 255).astype(np.uint8)

        positions_vertices = np.array(list_centroids)
        color_vertices = (np.array(list_colors_vertices)* 255).astype(np.uint8)

        pcd_segmentation = o3d.geometry.PointCloud()
        for pcd in PCDs:
            pcd_segmentation += pcd

        pcd_segmentation_positions = np.asarray(pcd_segmentation.points)
        pcd_segmentation_colors = (np.asarray(pcd_segmentation.colors) * 255).astype(np.uint8)

        v.add_points('Original point cloud', point_positions, point_colors, point_size=15, visible=False) # TOSET you can change the size of the points
        v.add_points('Nodes', transform_points(positions_vertices, centroid), color_vertices, point_size=500, visible=False) # TOSET you can change the size of the points
        v.add_points('Segmentation', transform_points(pcd_segmentation_positions, centroid), pcd_segmentation_colors, point_size=15, visible=False) # TOSET you can change the size of the points

        # Add the edges

        list_colors_edges = [[1, 0, 1] for index in range(len(list_pairs_edges))] # TOSET you can change the color of the edges
        lines_start = np.array(list(map(lambda x: x[0], list_pairs_edges)))
        lines_end = np.array(list(map(lambda x: x[1], list_pairs_edges)))
        v.add_lines(name='Edges', lines_start=transform_points(lines_start, centroid), lines_end=transform_points(lines_end, centroid), colors=np.array(list_colors_edges), visible=True)


        # Add the labels

        if wantLabels:
            v.add_labels(name ='Labels',
                            labels = [label.lower() for label in list_labels], # TOSET: if you want in capital letters or not
                            positions = transform_points(positions_vertices, centroid),
                            colors = color_vertices,
                            visible=False)

        v.save(folder_path)




def update_changes(old_SceneGraph, new_SceneGraph, list_newID_added, list_oldID_removed, dict_oldIDnewID_moved, dict_oldIDnewID_still):
    # Apart from nodes that have not been analysed, everything that has not been added, removed or moved stayed still
    # TODO: with other pieces of code that I had written, I may also easily store the transformation matrix for the objects that have been moved

    # Set the colors and create a deepcopy of the two scenegraphs

    color_added = [2, 196, 66] #'#02c442' # green
    color_removed = [139, 0, 0] #'#8B0000' # red
    color_moved = [255, 140, 0] #'#FF8C00' # orange
    color_still = [135, 206, 250] #'#87CEFA' # light blue
    color_notChecked = [96, 96, 96]  #'#606060' # grey

    deepcopy_old_SceneGraph = copy.deepcopy(old_SceneGraph)
    deepcopy_new_SceneGraph = copy.deepcopy(new_SceneGraph)

    # Add the information to old_SceneGraph

    for objectID in deepcopy_old_SceneGraph.nodes:

        if objectID in list_oldID_removed:
            deepcopy_old_SceneGraph.nodes[objectID]['color update'] = color_removed
            break

        if objectID in dict_oldIDnewID_moved:
            deepcopy_old_SceneGraph.nodes[objectID]['color update'] = color_moved
            deepcopy_old_SceneGraph.nodes[objectID]['ID in the new SceneGraph'] = dict_oldIDnewID_moved[objectID]
            break
        
        if objectID in dict_oldIDnewID_still:
            deepcopy_old_SceneGraph.nodes[objectID]['color update'] = color_still
            break

        deepcopy_old_SceneGraph.nodes[objectID]['color update'] = color_notChecked # if we arrive here, the node simply was not analysed


    # Add the information to new_SceneGraph

    def get_key(dict, value_to_find):
        for key, value in dict.items():
            if value == value_to_find:
                return key


    for objectID in deepcopy_new_SceneGraph.nodes:

        if objectID in list_newID_added:
            deepcopy_new_SceneGraph.nodes[objectID]['color update'] = color_added
            break

        if objectID in dict_oldIDnewID_moved.values():
            deepcopy_new_SceneGraph.nodes[objectID]['color update'] = color_moved
            deepcopy_new_SceneGraph.nodes[objectID]['ID in the old SceneGraph'] = get_key(dict_oldIDnewID_moved, objectID)
            break
        
        if objectID in dict_oldIDnewID_still.values():
            deepcopy_new_SceneGraph.nodes[objectID]['color update'] = color_still
            break

        deepcopy_new_SceneGraph.nodes[objectID]['color update'] = color_notChecked # if we arrive here, the node simply was not analysed


    return deepcopy_old_SceneGraph, deepcopy_new_SceneGraph






if __name__ == '__main__':
    path_plyFile = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/frl_apartment_0_withIDs.ply'
    path_colorDict_frlApartments = '/local/home/gmarsich/Desktop/data_Replica/colorDict_frlApartments.json'

    path_listInstances = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/list_instances.txt'
    path_distanceMatrix = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/matrix_distances_file<function distance_Euclidean_closest_points at 0x7f774e90e830>.txt'
    path_associationsObjectIdIndex = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/associations_objectIdIndex.json'

    
    graph = SceneGraph()
    graph.populate_SceneGraph(path_plyFile, path_distanceMatrix = path_distanceMatrix, path_associationsObjectIdIndex = path_associationsObjectIdIndex, path_colorDict_frlApartments = path_colorDict_frlApartments, path_listInstances = path_listInstances)
    graph.print_info_node('4')
    list_IDs = [4, 5, 10, 12]
    list_vertices, list_centroids, list_colors_vertices, list_labels, PCDs, list_edges, list_pairs_edges = graph.get_visualisation_SceneGraph(list_IDs, threshold=5, color = 'absoluteColor')
    graph.draw_SceneGraph_PyViz3D(list_centroids, list_colors_vertices, list_labels, list_pairs_edges, PCDs, wantLabels = True)
    

