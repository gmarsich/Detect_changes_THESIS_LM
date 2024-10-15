# COMMENTED

# environment: sceneGraphs_groundTruth_Replica

'''This script enquires about the importance of the PCA components. It generates a dictionary with all the information (on the 6 apartments)
Given the key, saves a plot of a frl apartment showing the importance of each component in the PCA.
The importance is given by averaging the explained variance across all the instances in the analysed frl apartment.'''

import os
import sys
grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, grandparent_dir)

import open3d as o3d
import time
import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from SceneGraph import SceneGraph # local file


#
# Variables
#

basePath = '/local/home/gmarsich/Desktop/data_Replica'

needDictExplainedVariance = True # considers all the frl apartments
key_frl_apartment = '0'
savePlot = True # save the plot of the explained variance of a specific frl apartment


#
# Automatic variables
#

path_save_data = os.path.join(basePath, 'PCA_variance') # will be created it does not exist
path_explainedVariance = os.path.join(path_save_data, 'dict_explainedVariance.json')

# Get the paths of the scene graphs

list_paths_sceneGraphs = [os.path.join(basePath, 'frl_apartment_0/Scene_Graphs/sceneGraph_GT'),
                    os.path.join(basePath, 'frl_apartment_1/Scene_Graphs/sceneGraph_GT'),
                    os.path.join(basePath, 'frl_apartment_2/Scene_Graphs/sceneGraph_GT'),
                    os.path.join(basePath, 'frl_apartment_3/Scene_Graphs/sceneGraph_GT'),
                    os.path.join(basePath, 'frl_apartment_4/Scene_Graphs/sceneGraph_GT'),
                    os.path.join(basePath, 'frl_apartment_5/Scene_Graphs/sceneGraph_GT'),]




#
# Do the computations. Statistics: how much is the variance explained by the components of the PCA?
#

def pca_embedding(pcd, n_components):
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    points_with_colors = np.hstack((points, colors))
    centered_points_with_colors = points_with_colors - np.mean(points_with_colors, axis=0) # substract the mean as required by PCA
    pca = PCA(n_components)
    embedding = pca.fit_transform(centered_points_with_colors)

    #print("Explained variance ratio by each PCA component: ", pca.explained_variance_ratio_)

    return pca, embedding




os.makedirs(path_save_data, exist_ok=True)


# Compute the dictionary

if needDictExplainedVariance:

    # Load the scene graphs

    list_sceneGraphs = []

    for path in list_paths_sceneGraphs:
        graph = SceneGraph()
        graph.load_SceneGraph(path)
        list_sceneGraphs.append(graph)


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

    compute_and_save_dictExplainedVariance(list_sceneGraphs)


    # TIMINGS:
    # frl_apartment_0: 1.455555 seconds
    # frl_apartment_1: 1.411105 seconds
    # frl_apartment_2: 1.505795 seconds
    # frl_apartment_3: 1.525883 seconds
    # frl_apartment_4: 1.434572 seconds
    # frl_apartment_5: 1.389904 seconds


# Save the plot of one frl apartment

if savePlot:

    with open(path_explainedVariance, 'r') as json_file:
        dict_explainedVariance = json.load(json_file)

    all_variance_lists = {}

    for key, value in dict_explainedVariance.items():
        all_variance_lists[key] = []

        for subkey, subvalue in value.items():
            all_variance_lists[key].append(subvalue)

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




