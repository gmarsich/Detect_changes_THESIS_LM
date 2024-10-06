'''This script provides some functions used by the PCA method.'''

import numpy as np
import copy
import open3d as o3d
from scipy.spatial import KDTree
from sklearn.decomposition import PCA
from .align_instancePCD import get_transformationMatrix # local file



# side function
# from: https://medium.com/@sim30217/chamfer-distance-4207955e8612
def chamfer_distance(A, B):
    """
    Computes the chamfer distance between two sets of points A and B.
    """
    tree = KDTree(B)
    dist_A = tree.query(A)[0]
    tree = KDTree(A)
    dist_B = tree.query(B)[0]
    return np.mean(dist_A) + np.mean(dist_B)


# side function
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

# side function
# Function to compute PCA embedding of a point cloud
def pca_embedding(pcd, n_components):
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    points_with_colors = np.hstack((points, colors))
    centered_points_with_colors = points_with_colors - np.mean(points_with_colors, axis=0) # substract the mean as required by PCA
    pca = PCA(n_components)
    embedding = pca.fit_transform(centered_points_with_colors)

    #print("Explained variance ratio by each PCA component: ", pca.explained_variance_ratio_)

    return pca, embedding



# Build the matrix with distances between instances and save the transformation matrices (obtained while trying to perform the alignments)
def get_distances_and_transformationMatrices(sceneGraph_a, sceneGraph_b, objectIDs_a, objectIDs_b, number_components):

    matrix_distances = np.full((len(objectIDs_a), len(objectIDs_b)), np.inf)
    dict_transformationMatrices = {}
    dict_associationsIndexObjectID_a = {}
    dict_associationsIndexObjectID_b = {}

    for index_a, objectID_a in enumerate(objectIDs_a):

        dict_transformationMatrices[index_a] = {}

        for index_b, objectID_b in enumerate(objectIDs_b):

            pcd_a = sceneGraph_a.get_pointCloud(objectID_a, wantVisualisation=False)
            pcd_b = sceneGraph_b.get_pointCloud(objectID_b, wantVisualisation=False)

            # Bring the pcd_a to have the centroid in the origin. pcd_b follows. Useful to then understand if there was a movement.
            # Then get the transformation matrix and transform pcd_b
            
            points = np.asarray(pcd_a.points)
            centroid = np.mean(points, axis=0)
            pcd_a.translate(-centroid)
            pcd_b.translate(-centroid)

            transformationMatrix = get_transformationMatrix(pcd_a, pcd_b, seeRenderings = False)
            pcd_b.transform(transformationMatrix)

            # Perform a downsampling. Compute the embeddings. Use Chamfer distance

            pcd_a_downsampled = farthest_point_sampling(pcd_a, n_samples=round(len(pcd_a.points)/10)) # 10 is chosen more or less randomly
            pcd_b_downsampled = farthest_point_sampling(pcd_b, n_samples=round(len(pcd_b.points)/10)) # 10 is chosen more or less randomly

            _, emb_a = pca_embedding(pcd_a_downsampled, n_components=number_components)
            _, emb_b = pca_embedding(pcd_b_downsampled, n_components=number_components)

            dist = chamfer_distance(emb_a, emb_b)

            matrix_distances[index_a][index_b] = dist
            dict_transformationMatrices[index_a][index_b] = transformationMatrix
            dict_associationsIndexObjectID_a[index_a] = objectID_a
            dict_associationsIndexObjectID_b[index_b] = objectID_b

            #print("Chamfer Distance (2D as 3D): ", objectID_a + "+" + objectID_b + "=" + str(dist))

    return matrix_distances, dict_transformationMatrices, dict_associationsIndexObjectID_a, dict_associationsIndexObjectID_b


# Retrieve the associations by iteratively finding the maximum value in the matrix. If there is a correspondance, find if it has been moved or not
def get_associations(threshold_correpondence, translation_threshold, rotation_threshold, matrix_distances, dict_transformationMatrices, dict_associationsIndexObjectID_a, dict_associationsIndexObjectID_b):

    list_newID_added = []
    list_oldID_removed = [] 
    dict_oldIDnewID_moved = {}
    dict_oldIDnewID_still = {}

    list_rows = []
    list_columns = []

    min_value = np.min(matrix_distances)

    while min < threshold_correpondence:
        
        row_index, col_index = np.unravel_index(np.argmin(matrix_distances), matrix_distances.shape) # get row and column of the min

        # Check if the instance stayed still of if it was moved

        movement_matrix = np.array(dict_transformationMatrices[row_index][col_index])

        translation = np.sqrt((movement_matrix[0, 3])**2 + (movement_matrix[1, 3])**2 + (movement_matrix[2, 3])**2)
        rotation = np.rad2deg(np.arccos((np.trace(movement_matrix[:3][:3]) - 1) / 2)) # from https://en.wikipedia.org/wiki/Rotation_matrix

        if translation < translation_threshold and rotation < rotation_threshold: # the instance remained still
            dict_oldIDnewID_still[dict_associationsIndexObjectID_a[row_index]] = dict_associationsIndexObjectID_b[col_index]
        else: # the instance was moved
            dict_oldIDnewID_moved[dict_associationsIndexObjectID_a[row_index]] = dict_associationsIndexObjectID_b[col_index]

        # Update the matrix

        matrix_distances[row_index, :] = np.inf
        matrix_distances[:, col_index] = np.inf
        list_rows.append(row_index)
        list_columns.append(col_index)

        min_value = np.min(matrix_distances)


    # Now only instances that do not have a correspondence remain. Transform the indexes in the objectIDs

    list_oldID_removed = [dict_associationsIndexObjectID_a[i] for i in range(len(matrix_distances)) if i not in list_rows]
    list_newID_added = [dict_associationsIndexObjectID_b[i] for i in range(len(matrix_distances[0])) if i not in list_columns]

    return list_newID_added, list_oldID_removed, dict_oldIDnewID_moved, dict_oldIDnewID_still
