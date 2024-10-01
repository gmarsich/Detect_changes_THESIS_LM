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

Since I specifically deal with Replica dataset, and in particular with the frl apartments, some preprocessing was performed to 

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
                random_dict[number] = np.array(random_array)
                break
    
    return random_dict



class SceneGraph(): # possible attributes: self.nodes, self.matrix_distances, self.associations_objectIdIndex
    def __init__(self):
        self.nodes = {}

    def populate_SceneGraph(self, path_plyFile, path_distanceMatrix = None, path_associationsIndexObjectID = None, path_listInstances = None, path_colorDict_frlApartments = None):
        # if matrixDistances.txt (together with associations_objectIdIndex.json) is provided, the attribute self.matrix_distances (that is the matrix with distances) will be added
        # if associations_objectIdIndex.json (together with matrixDistances.txt) is provided, the attribute self.associations_objectIdIndex (given an objectID, which is the its index in self.matrix_distances?) is added
        # if list_instances.txt is provided, the node will also contain the label of the instance
        # if colorDict_frlApartments.json is provided, the node will also contain the specific color associated to that label
        
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
            objectId = int(components[9])

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
            centroid = np.mean(points_geometric, axis=0)
            self.nodes[objectId]['centroid'] = centroid

        # Convert lists to numpy arrays
        for objectId, data in self.nodes.items():
            self.nodes[objectId]['points_geometric'] = np.array(data['points_geometric'])
            self.nodes[objectId]['points_color'] = np.array(data['points_color'])
            self.nodes[objectId]['points_normals'] = np.array(data['points_normals'])


        # Add a color for the segmentation

        list_numbers = list(self.nodes.keys())
        color_dict = create_colors_dict(list_numbers)

        for objectId in self.nodes:
            self.nodes[objectId]['ply_color'] = color_dict[objectId]


        # If path_distanceMatrix and path_associationsIndexObjectID are not None save the distances in a matrix
        
        if path_distanceMatrix and path_associationsIndexObjectID:
            matrix = []
            with open(path_distanceMatrix, 'r') as file:
                for line in file:
                    row = line.strip().split()
                    matrix.append([float(element) for element in row])

        self.matrix_distances = matrix

        with open(path_associationsIndexObjectID, 'r') as json_file:
            self.associations_objectIdIndex = json.load(json_file)



        # If path_listInstances is not None, associate the labels

        if path_listInstances:
            
            labels = {}

            with open(path_listInstances, 'r') as file:
                for line in file:
                    parts = line.strip().split() # split the line by tab or whitespace

                    objectId = int(parts[0])
                    label = parts[1]

                    labels[objectId] = label

            for objectId, data in self.nodes.items():
                if objectId in labels:
                    data['label'] = labels[objectId]
                else:
                    data['label'] = None


        # If path_colorDict_frlApartments is not None, associate the specific color to each label.
        # Be aware that you also need path_listInstances

        if path_colorDict_frlApartments and path_listInstances:
            with open(path_colorDict_frlApartments, 'r') as json_file:
                data_dict = json.load(json_file)

            for objectId, data in self.nodes.items():
                label = data[objectId]['label']
                data[objectId]['absolute color'] = data_dict[label]
    

    def load_SceneGraph(self, path_SceneGraph_folder):
        path_nodes = os.path.join(path_SceneGraph_folder, 'nodes.json')
        with open(path_nodes, 'r') as json_file: # populate self.nodes
            self.nodes = json.load(json_file)

        path_matrixDistances = os.path.join(path_SceneGraph_folder, 'matrix_distances.txt')
        if os.path.exists(path_matrixDistances):
            matrix = []
            with open(path_matrixDistances, 'r') as file: # populate self.matrix_distances
                for line in file:
                    row = line.strip().split()
                    matrix.append([float(element) for element in row])

            self.matrix_distances = matrix

            path_associationsIndexObjectID = os.path.join(path_SceneGraph_folder, 'associations_objectIdIndex.json')
            with open(path_associationsIndexObjectID, 'r') as json_file: # populate self.associations_objectIdIndex
                self.associations_objectIdIndex = json.load(json_file)
        
        return


    def print_info_node(self, objectId):
        print(self.nodes[objectId])


    def get_pointCloud(self, objectId, wantVisualisation = False):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(self.nodes[objectId]['points_geometric'])
        pcd.colors = o3d.utility.Vector3dVector(self.nodes[objectId]['points_color'] / 255) # normalise from range 0-255 to range 0-1
        pcd.normals = o3d.utility.Vector3dVector(self.nodes[objectId]['points_normals'])
        
        if wantVisualisation:
            o3d.visualization.draw_geometries([pcd])

        return pcd
    

    def update_changes(self, new_SceneGraph, list_newID_added, list_oldID_removed, dict_oldIDnewID_moved, dict_oldIDnewID_still): # be aware that the current SceneGraph will be replaced with the new one (and this will contain some additional information describing the changes)
        # everything that has not been added, removed or moved stayed still
        # TODO: with other pieces of code that I had written, I may also easily find the transformation matrix for the objects that have been moved

        # If it exist, clean all the information about a possible previous update
        # TODO

        # Set the colors

        color_added = '#02c442' # green
        color_removed = '#8B0000' # red
        color_moved = '#FF8C00' # orange
        color_still = '#87CEFA' # light blue
        color_notChecked = '#606060' # grey

        # Add the information to the current sceneGraph (oldSceneGraph)

        for objectID in self.nodes:

            if objectID in list_oldID_removed:
                self.nodes[objectID]['color update'] = color_removed
                break

            if objectID in dict_oldIDnewID_moved:
                self.nodes[objectID]['color update'] = color_moved
                self.nodes[objectID]['corresponding ID in the new SceneGraph'] = dict_oldIDnewID_moved[objectID]
                break
            
            if objectID in dict_oldIDnewID_still:
                self.nodes[objectID]['color update'] = color_still
                break

            self.nodes[objectID]['color update'] = color_notChecked # if we arrive here, the node simply was not analysed
    
        
        def get_key(dict, value_to_find):
            for key, value in dict.items():
                if value == value_to_find:
                    return key


        for objectID in new_SceneGraph.nodes:

            if objectID in list_newID_added:
                new_SceneGraph.nodes[objectID]['color update'] = color_added
                break

            if objectID in dict_oldIDnewID_moved.values():
                new_SceneGraph.nodes[objectID]['color update'] = color_moved
                new_SceneGraph.nodes[objectID]['corresponding ID in the new SceneGraph'] = get_key(dict_oldIDnewID_moved, objectID)
                break
            
            if objectID in dict_oldIDnewID_still:
                new_SceneGraph.nodes[objectID]['color update'] = color_still
                break

            new_SceneGraph.nodes[objectID]['color update'] = color_notChecked # if we arrive here, the node simply was not analysed


        # Update the current SceneGraph

        old_SceneGraph = copy.deepcopy(self)
        self = new_SceneGraph

        return old_SceneGraph, new_SceneGraph # be aware that now in the current object of SceneGraph the newSceneGraph is stored!
    

    def save_SceneGraph(self):
        # Create the folder where to store the data

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
                text_file.write(self.matrix_distances)

        if self.associations_objectIdIndex:
            with open(os.path.join(folder_path, 'associations_objectIdIndex.json'), 'w') as json_file: # save self.associations_objectIdIndex if it exists
                json.dump(self.associations_objectIdIndex, json_file, indent=4)

        # Write a message to reassure the user

        print(f'The files composing the scene graphs were saved to: {folder_path}') 

        return
    

    def get_visualisation_SceneGraph(self, list_IDs, color = 'absoluteColor'):
        # color: 'withUpdates' (show how the objects changed), 'randomColor' (given by self.nodes[objectId]['ply_color']), 'absoluteColor' (given by self.nodes[objectId]['absolute color'])
        



        return SG
    

    def draw_SceneGraph_PyViz3D(self):
        pass


if __name__ == '__main__':
    path_plyFile = '/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/withPCA/preprocessing/results/frl_apartment_0_withIDs.ply'
    path_listInstances = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/list_instances.txt'

    graph = SceneGraph(path_plyFile, path_listInstances)
    graph.print_info_node(4)
    _ = graph.get_pointCloud(4, True)


