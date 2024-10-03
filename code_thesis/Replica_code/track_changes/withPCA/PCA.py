'''I input it takes 2 sceneGraph objects and for each one a list of IDs of instances that one wants to compare.
PCA is applied to TODO'''

from code_thesis.Replica_code.SceneGraph import sceneGraph # local file
from align_instancePCD import get_transformationMatrix # local file
import numpy as np
from sklearn.decomposition import PCA
import open3d as o3d
from sklearn.metrics.pairwise import cosine_similarity


#
# Variables
#

path_plyFile_0 = '/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/withPCA/preprocessing/results/frl_apartment_0_withIDs.ply'
path_listInstances_0 = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/list_instances.txt'
path_plyFile_1 = '/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/withPCA/preprocessing/results/frl_apartment_1_withIDs.ply'
path_listInstances_1 = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/list_instances.txt'

objectIDs_0 = [34, 39, 27, 103, 38, 164] # 1: # bike, bike, ceiling, sofa, cup, sink
objectIDs_1 = [77, 93, 10, 4, 66, 59] # 0: bike, bike, ceiling, sofa, mat, book

objectID_0 = 4
objectID_1 = 121

number_components = 2



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


def downsample_pair_pcd(pcd_0, pcd_1):
    num_points_0 = len(pcd_0.points)
    num_points_1 = len(pcd_1.points)

    if num_points_0 > num_points_1:
        pcd_0_downsampled = farthest_point_sampling(pcd_0, num_points_1)
        pcd_1_downsampled = pcd_1
    else:
        pcd_1_downsampled = farthest_point_sampling(pcd_1, num_points_0)
        pcd_0_downsampled = pcd_0

    return pcd_0_downsampled, pcd_1_downsampled


#
# Performing PCA and comparing the results
#

# Load the scene graph and the point clouds. Apply the tranformation to try to align the two point clouds

scene_graph_0 = sceneGraph(path_plyFile_0, path_listInstances_0)
scene_graph_1 = sceneGraph(path_plyFile_1, path_listInstances_1)

pcd_0 = scene_graph_0.get_pointCloud(objectID_0)
pcd_1 = scene_graph_1.get_pointCloud(objectID_1)

transformationMatrix = get_transformationMatrix(pcd_0, pcd_1, seeRenderings = False) # a downsampling is performed internally to compute the matrix
pcd_1.transform(transformationMatrix)
o3d.visualization.draw_geometries([pcd_0, pcd_1])


# Compute the embeddings; cosine similarity as a metric

pcd_0_downsampled, pcd_1_downsampled = downsample_pair_pcd(pcd_0, pcd_1) # so that the embeddings can be better compared. The new pcds have the same amount of points

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



