# environment: sceneGraphs_groundTruth_Replica

'''Collection of functions useful to get the segmentation ground truth of a Replica scene.'''

import numpy as np
from scipy.spatial import KDTree
import open3d as o3d
import json
import os
import random


#
# Possible distance metrics
#

def distance_Euclidean_centroids(centroid_1, centroid_2):
    # In case the centroids are lists
    centroid_1 = np.array(centroid_1)
    centroid_2 = np.array(centroid_2)

    distance = np.linalg.norm(centroid_1 - centroid_2)
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

def farthest_point_sampling(pcd, n_samples):
    random.seed(42)

    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    n_points = points.shape[0]
    
    sampled_indices = np.zeros(n_samples, dtype=int)
    sampled_indices[0] = np.random.randint(n_points) # randomly select the first point

    distances = np.full(n_points, np.inf)

    for i in range(1, n_samples):
        current_point = points[sampled_indices[i - 1]]
        distances = np.minimum(distances, np.linalg.norm(points - current_point, axis=1))
        sampled_indices[i] = np.argmax(distances) # select the farthest point

    # Create a new point cloud from the sampled points
    sampled_points = points[sampled_indices]
    sampled_colors = colors[sampled_indices]
    sampled_pcd = o3d.geometry.PointCloud()
    sampled_pcd.points = o3d.utility.Vector3dVector(sampled_points)
    sampled_pcd.colors = o3d.utility.Vector3dVector(sampled_colors)

    return sampled_pcd


def get_list_instances_complete(list_labels, list_points):
    info_dict = {info[0]: info[1] for info in list_labels}
    list_instances_complete = []
    
    for obj_id, points in list_points:
        if obj_id in info_dict:
            class_name = info_dict[obj_id]
        else:
            class_name = 'None'

        centroid = np.mean(points, axis=0)
        list_instances_complete.append([obj_id, class_name, centroid, points])  

    return list_instances_complete


def compute_distance_matrix(list_instances_complete, path_save_files, compute_distance):
    matrix_distances = np.full((len(list_instances_complete), len(list_instances_complete)), np.inf) # putting 0 instead of np.inf will lead to an approximation to integers...
    associations = {}

    for i in range(len(matrix_distances)):
        for j in range(i + 1, len(matrix_distances[0])): # the matrix is symmetric
            associations[list_instances_complete[i][0]] = str(i)

            if compute_distance == distance_Euclidean_centroids: # CAVEAT: the centroid that is used is an approximation, since we have downsampled the point clouds
                matrix_distances[i][j] = compute_distance(list_instances_complete[i][2], list_instances_complete[j][2])
            else:
                matrix_distances[i][j] = compute_distance(list_instances_complete[i][3], list_instances_complete[j][3])
            
            matrix_distances[j][i] = matrix_distances[i][j]


    # Save matrix_distances in a file
    with open(os.path.join(path_save_files, "matrix_distances_file" + str(compute_distance) + ".txt"), 'w') as file_matrix: #TODO: the name can be improved, due to str(compute_distance)
        file_matrix.write("\n")
        np.savetxt(file_matrix, matrix_distances, fmt='%.18e')

    # Save associations_objectIdIndex
    with open(os.path.join(path_save_files, 'associations_objectIdIndex.json'), 'w') as json_file:
        json.dump(associations, json_file, indent=4)

    # Save list_instances
    with open(os.path.join(path_save_files, "list_instances.txt"), 'w') as file_objects:
        for sublist in list_instances_complete:
            obj_id, class_name, _, _ = sublist
            file_objects.write(f"{obj_id}\t{class_name}\n")
    
    return matrix_distances