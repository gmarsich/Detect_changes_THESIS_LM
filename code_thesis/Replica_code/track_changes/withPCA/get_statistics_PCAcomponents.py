# environment: sceneGraphs_groundTruth_Replica

'''This script enquires about the importance of the PCA components. It generates and saves a plots (given the frl apartment) showing the importance of each component in the PCA.
The importance is given by averaging the explained variance across all the instances in the analysed frl apartment.'''

import os
import sys
grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, grandparent_dir)

import open3d as o3d
import time
import numpy as np
import json
from PCA import pca_embedding # local file
from SceneGraph import SceneGraph # local file


#
# Variables
#

basePath = '/local/home/gmarsich/Desktop/data_Replica'
path_save_data = os.path.join(basePath, 'PCA_variance') # will be created it does not exist

path_explainedVariance = os.path.join(path_save_data, '/dict_explainedVariance.json') # be aware that the folder should already exist!
needDictExplainedVariance = True
savePlot = True # save the plot of the explained variance
key_frl_apartment = '0'


#
# Do the computations. Statistics: how much is the variance explained by the components of the PCA?
#

os.makedirs(path_save_data, exist_ok=True)

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




