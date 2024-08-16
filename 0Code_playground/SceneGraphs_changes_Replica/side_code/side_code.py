# environment: sceneGraphs_groundTruth_Replica

'''Collection of function useful to get the segmentation ground truth of a Replica scene'''

import numpy as np
from scipy.spatial import KDTree


#
# Possible distance metrics
#

def distance_Euclidean_centerBoundingBoxes(center_1, center_2):
    distance = np.linalg.norm(center_1 - center_2)
    return distance


def distance_Euclidean_closest_points(list_points_1, list_points_2):
    tree = KDTree(list_points_2)
    min_distance = np.inf
    for point1 in list_points_1:
        dist, _ = tree.query(point1)
        if dist < min_distance:
            min_distance = dist
    return min_distance



#
# Other useful functions
#

def get_list_instances(list_info, list_points):
    list_instances = [] # will contain a list of [obj_id, class_name, center, points]

    for obj in list_info:
        obj_id = obj[0]
        class_name = obj[1]
        center = obj[2]
        if obj_id < len(list_points):
            list_instances.append([obj_id, class_name, np.array(center), list_points[obj_id]])        
    
    transposed_list_instances = [list(row) for row in zip(*list_instances)]

    return list_instances, transposed_list_instances


def compute_distance_matrix(list_instances, compute_distance):
    matrix_distances = np.full((len(list_instances), len(list_instances)), np.inf)

    for i in range(len(matrix_distances)):
        for j in range(i + 1, len(matrix_distances[0])): # the matrix is symmetric

            if compute_distance == distance_Euclidean_centerBoundingBoxes:
                matrix_distances[i][j] = compute_distance(list_instances[i][2], list_instances[j][2])
            else:
                matrix_distances[i][j] = compute_distance(list_instances[i][3], list_instances[j][3])
            
            matrix_distances[j][i] = matrix_distances[i][j]

    # Save matrix_distances in a file
    with open("matrix_distances_file.txt", 'w') as file_matrix:
        file_matrix.write("\n")
        np.savetxt(file_matrix, matrix_distances, fmt='%.18e')

    # Save list_instances (but just the list of [obj_id, class_name, center], so without the list_points)
    with open("list_objects.txt", 'w') as file_objects:
        list_instances_noPoints = [sublist[:-1] for sublist in list_instances]
        for sublist in list_instances_noPoints:
            obj_id, class_name, center = sublist
            center_str = ', '.join(f'{coord:.6f}' for coord in center)
            file_objects.write(f"{obj_id}\t{class_name}\t{center_str}\n")
    
    return matrix_distances