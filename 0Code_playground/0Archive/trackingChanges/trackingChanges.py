# environment: labelmaker

'''I have six frl apartments from the Replica dataset, and somehow I have the segmentation of each one of them.
I want to track how the instances have been moved, with scene graphs.'''

import class_sceneGraph


#
# Variables to set
#

path_to_matrixDistances_0 = '/local/home/gmarsich/Desktop/data_Replica/frl_0/matrix_distances_file_distance_Euclidean_centroids.txt'
path_to_listInstances_0 = '/local/home/gmarsich/Desktop/data_Replica/frl_0/list_instances.txt'
path_to_listPoints_0 = '/local/home/gmarsich/Desktop/data_Replica/frl_0/list_points.txt'

path_to_matrixDistances_1 = '/local/home/gmarsich/Desktop/data_Replica/frl_1/matrix_distances_file_distance_Euclidean_centroids.txt'
path_to_listInstances_1 = '/local/home/gmarsich/Desktop/data_Replica/frl_1/list_instances.txt'
path_to_listPoints_1 = '/local/home/gmarsich/Desktop/data_Replica/frl_1/list_points.txt'



#
# Build the scene graphs
#


sceneGraph_0 = class_sceneGraph.sceneGraph(list_instances, list_points, matrix_distances)

