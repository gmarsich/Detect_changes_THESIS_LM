# environment: sceneGraphs_groundTruth_Replica

'''In input it takes 2 SceneGraph objects and for each one a list of IDs of instances that one wants to compare.
PCA is applied to get the embeddings, that are then compared to find the associations. The output is made of four variables:
- list_newID_added
- list_oldID_removed
- dict_oldIDnewID_moved
- dict_oldIDnewID_still

'''

import os
import sys

grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, grandparent_dir)

from SceneGraph import SceneGraph # local file
from side_code.find_associations import get_distances_and_transformationMatrices, get_associations # local file
import numpy as np
from sklearn.decomposition import PCA
import open3d as o3d
from sklearn.metrics.pairwise import cosine_similarity
import time
import json
import matplotlib.pyplot as plt


#
# Variables
#

frl_apartment_a = 'frl_apartment_0'
frl_apartment_b = 'frl_apartment_1'

namePLY_a = frl_apartment_a + '_withIDs.ply' # _withIDs.ply: from the ground truth; _withIDs_LabelMaker.ply: from labelMaker
namePLY_b = frl_apartment_b + '_withIDs.ply' # _withIDs.ply: from the ground truth; _withIDs_LabelMaker.ply: from labelMaker

basePath = '/local/home/gmarsich/Desktop/data_Replica'

objectIDs_a = ['34', '39', '27', '103', '38', '164'] # 1: # bike, bike, ceiling, sofa, cup, sink
objectIDs_b = ['77', '93', '10', '4', '66', '59'] # 0: bike, bike, ceiling, sofa, mat, book

# objectID_a = str(93)
# objectID_b = str(39)

number_components = 2
threshold = 0.08
translation_threshold = 0.2 # in meters
rotation_threshold = 15 # in degrees
threshold_correpondence = 0.08



#
# Automatic variables: they should be fine like this. CHANGE IF YOU WANT THE GROUND TRUTH OF LABELMAKER; CHANGE THE MATRIX DISTANCE
#

path_colorDict_frlApartments = os.path.join(basePath, 'colorDict_frlApartments.json')

path_plyFile_a = os.path.join(basePath, frl_apartment_a, namePLY_a)
path_listInstances_a = os.path.join(basePath, frl_apartment_a, 'list_instances.txt')
path_distanceMatrix_a = os.path.join(basePath, frl_apartment_a, 'matrix_distances_file<function distance_Euclidean_closest_points at 0x7f774e90e830>.txt') 
path_associationsObjectIdIndex_a = os.path.join(basePath, frl_apartment_a, 'associations_objectIdIndex.json')

path_plyFile_b = os.path.join(basePath, frl_apartment_b, namePLY_b)
path_listInstances_b = os.path.join(basePath, frl_apartment_b, 'list_instances.txt')
path_distanceMatrix_b = os.path.join(basePath, frl_apartment_b, 'matrix_distances_file<function distance_Euclidean_closest_points at 0x7f774e90e830>.txt') 
path_associationsObjectIdIndex_b = os.path.join(basePath, frl_apartment_b, 'associations_objectIdIndex.json')



#
# Some useful functions
#

# Function to compute PCA embedding of a point cloud
def pca_embedding(pcd, n_components=3):
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    points_with_colors = np.hstack((points, colors))
    centered_points_with_colors = points_with_colors - np.mean(points_with_colors, axis=0) # substract the mean as required by PCA
    pca = PCA(n_components)
    embedding = pca.fit_transform(centered_points_with_colors)

    #print("Explained variance ratio by each PCA component: ", pca.explained_variance_ratio_)

    return pca, embedding



#
# Performing PCA and comparing the results
#

# Load the scene graphs

sceneGraph_a = SceneGraph()
sceneGraph_a.populate_SceneGraph(path_plyFile_a, path_distanceMatrix = path_distanceMatrix_a, path_associationsObjectIdIndex = path_associationsObjectIdIndex_a,
                                 path_listInstances = path_listInstances_a, path_colorDict_frlApartments = path_colorDict_frlApartments)

sceneGraph_b = SceneGraph()
sceneGraph_b.populate_SceneGraph(path_plyFile_b, path_distanceMatrix = path_distanceMatrix_b, path_associationsObjectIdIndex = path_associationsObjectIdIndex_b,
                                 path_listInstances = path_listInstances_b, path_colorDict_frlApartments = path_colorDict_frlApartments)




matrix_distances, dict_transformationMatrices, dict_associationsIndexObjectID_a, dict_associationsIndexObjectID_b = get_distances_and_transformationMatrices(sceneGraph_a, sceneGraph_b, objectIDs_a, objectIDs_b, number_components)

list_newID_added, list_oldID_removed, dict_oldIDnewID_moved, dict_oldIDnewID_still = get_associations(threshold_correpondence, translation_threshold, rotation_threshold,
                                                                                                      matrix_distances, dict_transformationMatrices,
                                                                                                      dict_associationsIndexObjectID_a, dict_associationsIndexObjectID_b)

















# # Compute the embeddings; cosine similarity as a metric

# def downsample_pair_pcd(pcd_a, pcd_b):
#     num_points_a = len(pcd_a.points)
#     num_points_b = len(pcd_b.points)

#     if num_points_a > num_points_b:
#         pcd_a_downsampled = farthest_point_sampling(pcd_a, num_points_b)
#         pcd_b_downsampled = pcd_b
#     else:
#         pcd_b_downsampled = farthest_point_sampling(pcd_b, num_points_a)
#         pcd_a_downsampled = pcd_a

#     return pcd_a_downsampled, pcd_b_downsampled



# pcd_a_downsampled, pcd_b_downsampled = downsample_pair_pcd(pcd_a, pcd_b) # so that the embeddings can be better compared. The new pcds have the same amount of points

# pcd_a_downsampled = farthest_point_sampling(pcd_a_downsampled, n_samples=1000)
# pcd_b_downsampled = farthest_point_sampling(pcd_b_downsampled, n_samples=1000)

# _, emb_a = pca_embedding(pcd_a_downsampled, n_components=number_components)
# _, emb_b = pca_embedding(pcd_b_downsampled, n_components=number_components)

# cos_sim = cosine_similarity(emb_a, emb_b)
# cos_sim_max = []
# while cos_sim.size > 0:
#     max_value = np.max(cos_sim)
#     max_index = np.unravel_index(np.argmax(cos_sim), cos_sim.shape) # get row and column of the max

#     cos_sim_max.append(max_value)

#     cos_sim = np.delete(cos_sim, max_index[0], axis=0)  # remove the row
#     cos_sim = np.delete(cos_sim, max_index[1], axis=1)  # remove the column

# average_similarity = np.mean(cos_sim_max)
# print("Average Cosine Similarity:", average_similarity)



