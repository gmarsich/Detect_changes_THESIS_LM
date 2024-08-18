# environment: sceneGraphs_groundTruth_Replica

'''Define the class sceneGraph. An instance of this class is a scene graph.'''

import pyviz3d.visualizer as viz
import os
import numpy as np
import open3d as o3d


class sceneGraph:
    def __init__(self, list_instances, list_instancesPoints, matrix_distances): # the inputs are variables elaborated from the files list_instances.txt, list_points.txt and matrix_distances_file.txt
        self.build_nodes(self, list_instances, list_instancesPoints)
        self.build_edges(self, list_instances, matrix_distances)
    
    def build_nodes(self, list_instances, list_instancesPoints): # info on nodes are stored in a dictionary
        dict = {}

        for instance in list_instances:
            obj_id = instance[0]
            class_name = instance[1]
            centroid = instance[2]
            points = next((item[1] for item in list_instancesPoints if item[0] == obj_id), None) # in theory everything should work in the proper way, and no None should appear
            dict[obj_id] = {
                "class_name": class_name,
                "centroid": centroid,
                "points": points
            }

        self.nodes = dict

    
    def build_edges(self, list_instances, matrix_distances): # info on edges are stored in a dictionary
        adjacency_list = {}

        for i in range(len(list_instances)):
            obj_id_i = list_instances[i][0]  # obj_id of the i-th element
            adjacency_list[obj_id_i] = {}
            
            for j in range(len(list_instances)):
                if i != j:  # skip self-loops
                    obj_id_j = list_instances[j][0]  # obj_id of the j-th element
                    distance = matrix_distances[i][j]

                    adjacency_list[obj_id_i][obj_id_j] = distance

        self.edges = adjacency_list
        

