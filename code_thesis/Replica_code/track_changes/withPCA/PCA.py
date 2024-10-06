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
import open3d as o3d
from sklearn.metrics.pairwise import cosine_similarity
import time



start_time = time.time()

#
# Variables
#

frl_apartment_a = 'frl_apartment_0'
frl_apartment_b = 'frl_apartment_1'

nameSceneGraph = 'sceneGraph_GT' # depending if you basically have _LabelMaker or _GT

basePath = '/local/home/gmarsich/Desktop/data_Replica'

objectIDs_a = ['10', '4', '71', '77']
objectIDs_b = ['27', '103', '136', '34'] 


#
# Automatic variables
#

path_a = os.path.join(basePath, frl_apartment_a, 'Scene_Graphs', nameSceneGraph)
path_b = os.path.join(basePath, frl_apartment_b, 'Scene_Graphs', nameSceneGraph)


#
# Hardcoded conditions
#

number_components = 2
translation_threshold = 0.2 # in meters
rotation_threshold = 15 # in degrees
threshold_correpondence = 0.08



#
# Performing PCA and comparing the results
#

# Load the scene graphs

sceneGraph_a = SceneGraph()
sceneGraph_a.load_SceneGraph(path_a)

sceneGraph_b = SceneGraph()
sceneGraph_b.load_SceneGraph(path_b)




matrix_distances, dict_transformationMatrices, dict_associationsIndexObjectID_a, dict_associationsIndexObjectID_b = get_distances_and_transformationMatrices(sceneGraph_a, sceneGraph_b, objectIDs_a, objectIDs_b, number_components)

print('matrix_distances')
print(matrix_distances)

# print('dict_transformationMatrices')
# print(dict_transformationMatrices)

# print('dict_associationsIndexObjectID_a')
# print(dict_associationsIndexObjectID_a)

# print('dict_associationsIndexObjectID_b')
# print(dict_associationsIndexObjectID_b)

list_newID_added, list_oldID_removed, dict_oldIDnewID_moved, dict_oldIDnewID_still, dict_corr_oldNew_dist = get_associations(threshold_correpondence, translation_threshold, rotation_threshold,
                                                                                                      matrix_distances, dict_transformationMatrices,
                                                                                                      dict_associationsIndexObjectID_a, dict_associationsIndexObjectID_b)


print('list_newID_added')
print(list_newID_added)

print('list_oldID_removed')
print(list_oldID_removed)

print('dict_oldIDnewID_moved')
print(dict_oldIDnewID_moved)

print('dict_oldIDnewID_still')
print(dict_oldIDnewID_still)

print('dict_corr_oldNew_dist')
print(dict_corr_oldNew_dist)


end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")










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



