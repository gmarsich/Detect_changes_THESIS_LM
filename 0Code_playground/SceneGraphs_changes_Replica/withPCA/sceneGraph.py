''' Class sceneGraph: given as input a .ply with this header:
ply
format ascii 1.0
element vertex 1796927
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
property int objectId
end_header

builds the sceneGraph object.

'''
#TODO: insert edges
#TODO: add a function to color a set of nodes in a specific color (eg I may want to color in red all the nodes that have been removed)

import numpy as np
import open3d as o3d
import random


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



class sceneGraph():
    def __init__(self, path_plyFile, path_listInstances = None): # if list_instances.txt is provided, the node will also contain the label of the instance
        
        self.nodes = {}

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
            objectId = int(components[6])

            if objectId not in self.nodes.keys():
                self.nodes[objectId] = {
                    'points_geometric': [],
                    'points_color': [],
                    'centroid': None
                    }
            
            self.nodes[objectId]['points_geometric'].append([x, y, z])
            self.nodes[objectId]['points_color'].append([red, green, blue])
        
        for objectId, data in self.nodes.items():
            points_geometric = np.array(data['points_geometric'])
            centroid = np.mean(points_geometric, axis=0)
            self.nodes[objectId]['centroid'] = centroid

        # Convert lists to numpy arrays
        for objectId, data in self.nodes.items():
            self.nodes[objectId]['points_geometric'] = np.array(data['points_geometric'])
            self.nodes[objectId]['points_color'] = np.array(data['points_color'])


        # Add a color for the segmentation

        list_numbers = list(self.nodes.keys())
        color_dict = create_colors_dict(list_numbers)

        for objectId in self.nodes:
            self.nodes[objectId]['ply_color'] = color_dict[objectId]


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
    

    def print_info_node(self, objectId):
        print(self.nodes[objectId])


    def get_pointCloud(self, objectId, wantVisualisation = False):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(self.nodes[objectId]['points_geometric'])
        pcd.colors = o3d.utility.Vector3dVector(self.nodes[objectId]['points_color'] / 255) # normalise from range 0-255 to range 0-1

        if wantVisualisation:
            o3d.visualization.draw_geometries([pcd])

        return pcd


if __name__ == '__main__':
    path_plyFile = '/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/withPCA/preprocessing/results/frl_apartment_0_withIDs.ply'
    path_listInstances = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/list_instances.txt'

    graph = sceneGraph(path_plyFile, path_listInstances)
    graph.print_info_node(130)
    _ = graph.get_pointCloud(130)


