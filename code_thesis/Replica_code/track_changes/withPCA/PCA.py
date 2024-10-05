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


#
# Automatic variables: they should be fine like this
#

path_plyFile_a = os.path.join(basePath, frl_apartment_a, namePLY_a)
path_listInstances_a = os.path.join(basePath, frl_apartment_a, 'list_instances.txt')


path_plyFile_b = os.path.join(basePath, frl_apartment_b, namePLY_b)
path_listInstances_b = os.path.join(basePath, frl_apartment_b, 'list_instances.txt')



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

    return embedding


def farthest_point_sampling(pcd, n_samples):

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


def compute_and_save_dictExplainedVariance(list_sceneGraphs):
    for graph in list_sceneGraphs

    start_time = time.time()


    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.6f} seconds")



#
# Performing PCA and comparing the results
#

# Load the scene graph and the point clouds. Apply the tranformation to try to align the two point clouds

sceneGraph_a = SceneGraph()
sceneGraph_a.populate_SceneGraph(path_plyFile_a, path_listInstances=path_listInstances_a)
sceneGraph_b = SceneGraph()
sceneGraph_b.populate_SceneGraph(path_plyFile_b, path_listInstances=path_listInstances_b)

pcd_a = sceneGraph_a.get_pointCloud(objectID_a, wantVisualisation=True)
pcd_b = sceneGraph_b.get_pointCloud(objectID_b, wantVisualisation=True)


'''
transformationMatrix = get_transformationMatrix(pcd_a, pcd_b, seeRenderings = False) # a downsampling is performed internally to compute the matrix
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






# cos_sim_min = np.max(cos_sim, axis=1) # get the maximum value across each row
# average_similarity = np.mean(cos_sim_min)
# print("Average Cosine Similarity:", average_similarity)









# mean_emb_0 = np.mean(emb_0, axis=0)
# mean_emb_1 = np.mean(emb_1, axis=0)
# distance = np.linalg.norm(mean_emb_0 - mean_emb_1)
# print(distance)





# Euclidean distance



# Chamfer distance

# Hausdorff Distance

# Wasserstein Distance

# Kolmogorov-Smirnov (K-S) test


# TODO: downsampling



'''