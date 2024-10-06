# environment: sceneGraphs_groundTruth_Replica

'''In input it takes 2 SceneGraph objects and for each one a list of IDs of instances that one wants to compare.
PCA is applied to TODO'''
import os
import sys

grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, grandparent_dir)

from SceneGraph import SceneGraph # local file
from align_instancePCD import get_transformationMatrix # local file
import numpy as np
from sklearn.decomposition import PCA
import open3d as o3d
from sklearn.metrics.pairwise import cosine_similarity
import time
import json
import matplotlib.pyplot as plt
import copy


#
# Variables
#

frl_apartment_a = 'frl_apartment_0'
frl_apartment_b = 'frl_apartment_1'

namePLY_a = frl_apartment_a + '_withIDs.ply' # _withIDs.ply: from the ground truth; _withIDs_LabelMaker.ply: from labelMaker
namePLY_b = frl_apartment_b + '_withIDs.ply' # _withIDs.ply: from the ground truth; _withIDs_LabelMaker.ply: from labelMaker

basePath = '/local/home/gmarsich/Desktop/data_Replica'

objectIDs_a = [34, 39, 27, 103, 38, 164] # 1: # bike, bike, ceiling, sofa, cup, sink
objectIDs_b = [77, 93, 10, 4, 66, 59] # 0: bike, bike, ceiling, sofa, mat, book

objectID_a = str(4)
objectID_b = str(121)

number_components = 2


path_explainedVariance = os.path.join(basePath, 'PCA_variance/dict_explainedVariance.json') # be aware that the folder should already exist!
needDictExplainedVariance = False
savePlot = False # save the plot of the explained variance
key_frl_apartment = '0'


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


def farthest_point_sampling(pcd, n_samples):

    sampled_pcd = copy.deepcopy(pcd)

    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    n_points = points.shape[0]

    if n_points > n_samples:
    
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


def downsample_pair_pcd(pcd_a, pcd_b):
    num_points_a = len(pcd_a.points)
    num_points_b = len(pcd_b.points)

    if num_points_a > num_points_b:
        pcd_a_downsampled = farthest_point_sampling(pcd_a, num_points_b)
        pcd_b_downsampled = pcd_b
    else:
        pcd_b_downsampled = farthest_point_sampling(pcd_b, num_points_a)
        pcd_a_downsampled = pcd_a

    return pcd_a_downsampled, pcd_b_downsampled


def compute_and_save_dictExplainedVariance(list_sceneGraphs): # for ground truth
    dict_explainedVariance = {}
    for index, graph in enumerate(list_sceneGraphs):
        start_time = time.time()

        dict_explainedVariance[index] = {}
        
        for objectId in graph.nodes.keys():
            if graph.nodes[objectId]['label'] != 'None':
                pcd_object = o3d.geometry.PointCloud()
                pcd_object.points = o3d.utility.Vector3dVector(np.array(graph.nodes[objectId]['points_geometric']))
                pcd_object.colors = o3d.utility.Vector3dVector(np.array(graph.nodes[objectId]['points_color']) / 255)
                pca, _ = pca_embedding(pcd_object, n_components=6)
                dict_explainedVariance[index][objectId] = list(pca.explained_variance_ratio_)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.6f} seconds")

    
    with open(path_explainedVariance, 'w') as json_file:
        json.dump(dict_explainedVariance, json_file, indent=4)



#
# Statistics: how much is the variance explained by the components of the PCA?
#

if needDictExplainedVariance:

    sceneGraph_a = SceneGraph()
    sceneGraph_a.populate_SceneGraph(os.path.join(basePath, 'frl_apartment_0/frl_apartment_0_withIDs.ply'), path_listInstances=os.path.join(basePath, 'frl_apartment_0/list_instances.txt'))
    sceneGraph_b = SceneGraph()
    sceneGraph_b.populate_SceneGraph(os.path.join(basePath, 'frl_apartment_1/frl_apartment_1_withIDs.ply'), path_listInstances=os.path.join(basePath, 'frl_apartment_1/list_instances.txt'))
    sceneGraph_c = SceneGraph()
    sceneGraph_c.populate_SceneGraph(os.path.join(basePath, 'frl_apartment_2/frl_apartment_2_withIDs.ply'), path_listInstances=os.path.join(basePath, 'frl_apartment_2/list_instances.txt'))
    sceneGraph_d = SceneGraph()
    sceneGraph_d.populate_SceneGraph(os.path.join(basePath, 'frl_apartment_3/frl_apartment_3_withIDs.ply'), path_listInstances=os.path.join(basePath, 'frl_apartment_3/list_instances.txt'))
    sceneGraph_e = SceneGraph()
    sceneGraph_e.populate_SceneGraph(os.path.join(basePath, 'frl_apartment_4/frl_apartment_4_withIDs.ply'), path_listInstances=os.path.join(basePath, 'frl_apartment_4/list_instances.txt'))
    sceneGraph_f = SceneGraph()
    sceneGraph_f.populate_SceneGraph(os.path.join(basePath, 'frl_apartment_5/frl_apartment_5_withIDs.ply'), path_listInstances=os.path.join(basePath, 'frl_apartment_5/list_instances.txt'))

    compute_and_save_dictExplainedVariance([sceneGraph_a, sceneGraph_b, sceneGraph_c, sceneGraph_d, sceneGraph_e, sceneGraph_f])


    # TIMINGS:
    # frl_apartment_0: 1.477730 seconds
    # frl_apartment_1: 1.504907 seconds
    # frl_apartment_2: 1.444942 seconds
    # frl_apartment_3: 1.535040 seconds
    # frl_apartment_4: 1.534008 seconds
    # frl_apartment_5: 1.371782 seconds


if savePlot:

    with open(path_explainedVariance, 'r') as json_file:
        dict_explainedVariance = json.load(json_file)

    all_variance_lists = {}

    for key, value in dict_explainedVariance.items():
        all_variance_lists[key] = []

        for subkey, subvalue in value.items():
            all_variance_lists[key].append(subvalue)

    key_frl_apartment = '5'
    data = all_variance_lists[key_frl_apartment]

    data_array = np.array(data)

    mean_values = np.mean(data_array, axis=0)
    variance_values = np.var(data_array, axis=0)

    indices = np.arange(1, 7)  # 1 to 6

    plt.figure(figsize=(7, 5))
    plt.bar(indices - 0.2, mean_values, width=0.4, label='Mean', color='skyblue', align='center')

    plt.errorbar(indices, mean_values, yerr=np.sqrt(variance_values), fmt='o', color='orange', label='Standard deviation', capsize=5)

    plt.xlabel('Component of the PCA')
    plt.ylabel('Explained variance (range [0, 1])')
    plt.title('Explained variance for frl_apartment_' + key_frl_apartment)
    plt.xticks(indices)  # set x-ticks to match the indices
    plt.legend()
    plt.grid(axis='y')

    plt.tight_layout()
    plt.savefig(os.path.join(basePath, 'PCA_variance/explained_variance_frl_apartment_' + key_frl_apartment + '.png'), dpi=300)





#
# Performing PCA and comparing the results
#

# Load the scene graph and the point clouds. Apply the tranformation to try to align the two point clouds

sceneGraph_a = SceneGraph()
sceneGraph_a.populate_SceneGraph(path_plyFile_a, path_distanceMatrix = path_distanceMatrix_a, path_associationsObjectIdIndex = path_associationsObjectIdIndex_a,
                                 path_listInstances = path_listInstances_a, path_colorDict_frlApartments = path_colorDict_frlApartments)

sceneGraph_b = SceneGraph()
sceneGraph_b.populate_SceneGraph(path_plyFile_b, path_distanceMatrix = path_distanceMatrix_b, path_associationsObjectIdIndex = path_associationsObjectIdIndex_b,
                                 path_listInstances = path_listInstances_b, path_colorDict_frlApartments = path_colorDict_frlApartments)








pcd_a = sceneGraph_a.get_pointCloud(objectID_a, wantVisualisation=True)
pcd_b = sceneGraph_b.get_pointCloud(objectID_b, wantVisualisation=True)



transformationMatrix = get_transformationMatrix(pcd_a, pcd_b, seeRenderings = False)
pcd_b.transform(transformationMatrix)
o3d.visualization.draw_geometries([pcd_a, pcd_b])




# Compute the embeddings; cosine similarity as a metric

pcd_0_downsampled, pcd_1_downsampled = downsample_pair_pcd(pcd_a, pcd_b) # so that the embeddings can be better compared. The new pcds have the same amount of points

pcd_0_downsampled = farthest_point_sampling(pcd_0_downsampled, n_samples=1000)
pcd_1_downsampled = farthest_point_sampling(pcd_1_downsampled, n_samples=1000)

emb_0 = pca_embedding(pcd_0_downsampled, n_components=number_components)
emb_1 = pca_embedding(pcd_1_downsampled, n_components=number_components)

# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(emb_0)
# pcd_1 = o3d.geometry.PointCloud()
# pcd_1.points = o3d.utility.Vector3dVector(emb_1)
# o3d.visualization.draw_geometries([pcd.paint_uniform_color([1, 0.706, 0]), pcd_1.paint_uniform_color([0, 0.651, 0.929])])

cos_sim = cosine_similarity(emb_0, emb_1)
cos_sim_max = []
while cos_sim.size > 0:
    max_value = np.max(cos_sim)
    max_index = np.unravel_index(np.argmax(cos_sim), cos_sim.shape) # get row and column of the max

    cos_sim_max.append(max_value)

    cos_sim = np.delete(cos_sim, max_index[0], axis=0)  # remove the row
    cos_sim = np.delete(cos_sim, max_index[1], axis=1)  # remove the column

average_similarity = np.mean(cos_sim_max)
print("Average Cosine Similarity:", average_similarity)



# Chamfer distance



# TODO: downsampling
