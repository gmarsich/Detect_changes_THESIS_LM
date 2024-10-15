# COMMENTED

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

from SceneGraph import SceneGraph, update_changes # local file
from side_code.find_associations import get_distances_and_transformationMatrices, get_associations # local file
import numpy as np
import open3d as o3d
from sklearn.metrics.pairwise import cosine_similarity
import time



start_time = time.time()

#
# Variables
#

frl_apartment_a = 'frl_apartment_4'
frl_apartment_b = 'frl_apartment_5'

nameSceneGraph = 'sceneGraph_GT' # depending if you basically have _LabelMaker or _GT

basePath = '/local/home/gmarsich/Desktop/data_Replica'

objectIDs_a = ['96', '186', '202', '137', '148', '222'] # refrigerator, sofa, ceiling, bike, bike, table
objectIDs_b = ['200', '21', '6', '185', '143', '134'] # refrigerator, sofa, ceiling, bike, table, cabinet

list_IDs_a = objectIDs_a # to visualise # TODO
list_IDs_b = objectIDs_b # to visualise # TODO

threshold_edges = 0.7 # in the scene graph, to see the edges

path_save_a = os.path.join(basePath, frl_apartment_a, 'sceneGraphs_changes') # if it does not exist, the folder will be created
path_save_b = os.path.join(basePath, frl_apartment_b, 'sceneGraphs_changes') # if it does not exist, the folder will be created


#
# Automatic variables
#

path_a = os.path.join(basePath, frl_apartment_a, 'Scene_Graphs', nameSceneGraph)
path_b = os.path.join(basePath, frl_apartment_b, 'Scene_Graphs', nameSceneGraph)

os.makedirs(path_save_a, exist_ok=True)
os.makedirs(path_save_b, exist_ok=True)

#
# Hardcoded conditions
#

number_components = 2
translation_threshold = 0.25 # in meters
rotation_threshold = 20 # in degrees
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

# print('matrix_distances')
# print(matrix_distances)
# print('dict_transformationMatrices')
# print(dict_transformationMatrices)
# print('dict_associationsIndexObjectID_a')
# print(dict_associationsIndexObjectID_a)
# print('dict_associationsIndexObjectID_b')
# print(dict_associationsIndexObjectID_b)

list_newID_added, list_oldID_removed, dict_oldIDnewID_moved, dict_oldIDnewID_still, dict_corr_oldNew_dist = get_associations(threshold_correpondence, translation_threshold, rotation_threshold,
                                                                                                      matrix_distances, dict_transformationMatrices,
                                                                                                      dict_associationsIndexObjectID_a, dict_associationsIndexObjectID_b)


# print('list_newID_added')
# print(list_newID_added)
# print('list_oldID_removed')
# print(list_oldID_removed)
# print('dict_oldIDnewID_moved')
# print(dict_oldIDnewID_moved)
# print('dict_oldIDnewID_still')
# print(dict_oldIDnewID_still)
# print('dict_corr_oldNew_dist')
# print(dict_corr_oldNew_dist)


end_time = time.time()
elapsed_time = end_time - start_time
print(f"\n\nElapsed time: {elapsed_time:.6f} seconds")



#
# Visualise the scene graphs with changes
#

deepcopy_old_SceneGraph, deepcopy_new_SceneGraph = update_changes(sceneGraph_a, sceneGraph_b, list_newID_added, list_oldID_removed, dict_oldIDnewID_moved, dict_oldIDnewID_still)

_, list_centroids_a, list_colors_vertices_a, list_labels_a, PCDs_a, list_pairs_edges_a = deepcopy_old_SceneGraph.get_visualisation_SceneGraph(list_IDs_a, threshold_edges, color = 'withUpdates')
_, list_centroids_b, list_colors_vertices_b, list_labels_b, PCDs_b, list_pairs_edges_b = deepcopy_new_SceneGraph.get_visualisation_SceneGraph(list_IDs_b, threshold_edges, color = 'withUpdates')


deepcopy_old_SceneGraph.draw_SceneGraph_PyViz3D(list_centroids_a, list_colors_vertices_a, list_labels_a, list_pairs_edges_a, PCDs_a, path_save_a, wantLabels = True)
deepcopy_new_SceneGraph.draw_SceneGraph_PyViz3D(list_centroids_b, list_colors_vertices_b, list_labels_b, list_pairs_edges_b, PCDs_b, path_save_b, wantLabels = True)


print('\nlist_newID_added:')
print(list_newID_added)
print('\nlist_oldID_removed:')
print(list_oldID_removed)
print('\ndict_oldIDnewID_moved:')
print(dict_oldIDnewID_moved)
print('\ndict_oldIDnewID_still:')
print(dict_oldIDnewID_still)
print('\ndict_corr_oldNew_dist:')
print(dict_corr_oldNew_dist)




# IMPORTANT:
# After you obtained the scene graphs, follow the instructions that appear in the terminal to visualise them. You should act in the sceneGraphs_groundTruth_Replica environment.
# Additionally, you may need to use two different browsers (e.g., Chrome and Edge), one for a scene graph and the other for the other rendering













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



