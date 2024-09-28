'''I input it takes 2 sceneGraph objects and for each one a list of IDs of instances that one wants to compare.
PCA is applied to TODO'''

from sceneGraph import sceneGraph # local file
from alignPCD import get_transformationMatrix # local file
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
    n_points = points.shape[0]
    
    sampled_indices = np.zeros(n_samples, dtype=int)
    sampled_indices[0] = np.random.randint(n_points) # randomly select the first point

    distances = np.full(n_points, np.inf)

    for i in range(0, n_samples):
        # Update distances for the current selected point
        current_point = points[sampled_indices[i]]
        distances = np.minimum(distances, np.linalg.norm(points - current_point, axis=1))
        
        # Select the farthest point
        sampled_indices[i] = np.argmax(distances)

    # Create a new point cloud from the sampled points
    sampled_points = points[sampled_indices]
    sampled_pcd = o3d.geometry.PointCloud()
    sampled_pcd.points = o3d.utility.Vector3dVector(sampled_points)

    return sampled_pcd



#
# Performing PCA and comparing the results
#

scene_graph_0 = sceneGraph(path_plyFile_0, path_listInstances_0)
scene_graph_1 = sceneGraph(path_plyFile_1, path_listInstances_1)

pcd_0 = scene_graph_0.get_pointCloud(4)
pcd_1 = scene_graph_1.get_pointCloud(121)

transformationMatrix = get_transformationMatrix(pcd_0, pcd_1, seeRenderings = False) # a downsampling is performed internally to compute the matrix
pcd_1.transform(transformationMatrix)
o3d.visualization.draw_geometries([pcd_0, pcd_1])

emb_0 = pca_embedding(pcd_0)
emb_1 = pca_embedding(pcd_1)


pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(emb_1)
o3d.visualization.draw_geometries([pcd])








mean_emb_0 = np.mean(emb_0, axis=0)
mean_emb_1 = np.mean(emb_1, axis=0)
distance = np.linalg.norm(mean_emb_0 - mean_emb_1)
print(distance)


# Euclidean distance

# Cosine similarity

# Chamfer distance


# TODO: downsampling



