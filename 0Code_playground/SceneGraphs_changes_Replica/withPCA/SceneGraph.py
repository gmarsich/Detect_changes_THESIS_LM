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

Since I specifically deal with Replica dataset, and in particular with the frl apartments. Some preprocessing was performed to get the things in a way I liked.

'''

import numpy as np
import open3d as o3d
import random
import json
from datetime import datetime
import os
import copy


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



class SceneGraph(): # possible attributes: self.nodes, self.matrix_distances, self.associations_objectIdIndex
    # OK
    def __init__(self):
        self.nodes = {}

    # OK
    def populate_SceneGraph(self, path_plyFile, path_distanceMatrix = None, path_associationsObjectIdIndex = None, path_listInstances = None, path_colorDict_frlApartments = None):
        # path_distanceMatrix: if matrixDistances.txt (together with associations_objectIdIndex.json) is provided, the attribute self.matrix_distances (that is the matrix with distances) will be added
        # path_associationsObjectIdIndex: if associations_objectIdIndex.json (together with matrixDistances.txt) is provided, the attribute self.associations_objectIdIndex (given an objectID, which is the its index in self.matrix_distances?) is added
        # path_listInstances: if list_instances.txt is provided, the node will also contain the label of the instance
        # path_colorDict_frlApartments: if colorDict_frlApartments.json is provided, the node will also contain the specific color associated to that label
        
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
                data['absolute color'] = data_dict[label]
                self.nodes[objectId]['absolute color'] = data['absolute color']
    
    # OK
    def load_SceneGraph(self, path_SceneGraph_folder):
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
    
    # TODO
    def get_visualisation_SceneGraph(self, list_IDs, threshold, color = 'absoluteColor'):
        # color: 'withUpdates' (show how the objects changed), 'randomColor' (given by self.nodes[objectId]['ply_color']), 'absoluteColor' (given by self.nodes[objectId]['absolute color'])
        
        #return SG
        pass
    
    # TODO
    def draw_SceneGraph_PyViz3D(self):
        pass




def update_changes(old_SceneGraph, new_SceneGraph, list_newID_added, list_oldID_removed, dict_oldIDnewID_moved, dict_oldIDnewID_still):
    # Apart from nodes that have not been analysed, everything that has not been added, removed or moved stayed still
    # TODO: with other pieces of code that I had written, I may also easily store the transformation matrix for the objects that have been moved

    # Set the colors and create a deepcopy of the two scenegraphs

    color_added = '#02c442' # green
    color_removed = '#8B0000' # red
    color_moved = '#FF8C00' # orange
    color_still = '#87CEFA' # light blue
    color_notChecked = '#606060' # grey

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
    path_plyFile = '/local/home/gmarsich/Desktop/results/frl_apartment_0_withIDs.ply'
    path_colorDict_frlApartments = '/local/home/gmarsich/Desktop/Thesis/code_thesis/Replica_code/colorDict_frlApartments.json'

    path_listInstances = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/list_instances.txt'
    path_distanceMatrix = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/matrix_distances_file<function distance_Euclidean_closest_points at 0x7f0170ba6830>.txt'
    path_associationsObjectIdIndex = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/associations_objectIdIndex.json'

    
    graph = SceneGraph()
    # graph.populate_SceneGraph(path_plyFile, path_distanceMatrix = path_distanceMatrix, path_associationsObjectIdIndex = path_associationsObjectIdIndex, path_colorDict_frlApartments = path_colorDict_frlApartments, path_listInstances = path_listInstances, )
    # graph.print_info_node('12')
    # _ = graph.get_pointCloud('4', True)
    #graph.save_SceneGraph()
    graph.load_SceneGraph('/local/home/gmarsich/Desktop/sceneGraph_20241002_214521')
    graph.print_info_node('12')
    _ = graph.get_pointCloud('4', True)

    

