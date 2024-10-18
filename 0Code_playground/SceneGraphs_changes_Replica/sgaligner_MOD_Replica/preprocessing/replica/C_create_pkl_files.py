'''preprocess.py but for Replica.
Given a scene, the .pkl file will be created.'''

import numpy as np
import os
import json
import pickle
import time


start_time = time.time()

#
# Variables
#

base_path = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_5/SGAligner'
list_resolutions = [64, 128, 256, 512]
path_to_npy = os.path.join(base_path, 'data.npy')
path_objData = os.path.join(base_path, 'objects.json')
path_save_pkl_file = os.path.join(base_path, 'data_dict.pkl')


#
# Build the dictionary data_dict
#

# side function. Taken from utils/point_cloud.py
def pcl_farthest_sample(point, npoint, return_idxs = False):
    """
    Input:
        xyz: pointcloud data, [N, D]
        npoint: number of samples
    Return:
        centroids: sampled pointcloud index, [npoint, D]
    """
    N, D = point.shape
    if N < npoint:
        indices = np.random.choice(point.shape[0], npoint)
        point = point[indices]
        return point

    xyz = point[:, :3]
    centroids = np.zeros((npoint,))
    distance = np.ones((N,)) * 1e10
    farthest = np.random.randint(0, N)
    for i in range(npoint):
        centroids[i] = farthest
        centroid = xyz[farthest, :]
        dist = np.sum((xyz - centroid) ** 2, -1)
        mask = dist < distance
        distance[mask] = dist[mask]
        farthest = np.argmax(distance, -1)
    point = point[centroids.astype(np.int32)]

    if return_idxs: return point, centroids.astype(np.int32)
    return point



def get_data_dict(path_to_npy, obj_data, list_resolutions):
    '''Get, for the dictionary:
        'obj_points' # something like: data_dict['object_points'][pc_resolution][i]
        'ei' # id (as in objects.json) of the instances in the scene
    '''

    # Load the point cloud data from file
    ply_data = np.load(path_to_npy)
    points = np.stack([ply_data['x'], ply_data['y'], ply_data['z']]).transpose((1, 0))

    # Initialize the dictionary to store object points for different resolutions
    object_points = {}
    for pc_resolution in list_resolutions:
        object_points[pc_resolution] = []

    # Extract object data from obj_data
    object_data = obj_data['objects'] # obj_data['objects'][i] is the i-th dictionary, with info on a specific instance. The value of count in that dictionary is i

    objectIDs = []
    # Iterate through each object to collect point cloud data
    for idx, object in enumerate(object_data):

        object_id = int(object['id'])
        objectIDs.append(object_id)

        # Get the points belonging to the current object
        obj_pt_idx = np.where(ply_data['objectId'] == object_id) # indexes of the points in the pcd corresponding to a specific ID
        obj_pcl = points[obj_pt_idx] # array with points of the pcd of a specific instance, the one of id object_id

        # if object_id == 154:
        #     pcd = o3d.geometry.PointCloud()
        #     pcd.points = o3d.utility.Vector3dVector(obj_pcl)
        #     axis = o3d.geometry.TriangleMesh.create_coordinate_frame(
        #         size=1.0,  # Size of the axis
        #         origin=[0, 0, 0]  # Origin point of the axis
        #     )
        #     o3d.visualization.draw_geometries([pcd.paint_uniform_color([0, 0.651, 0.929]), axis])

        # Skip objects with fewer points than the minimum required
        # if obj_pcl.shape[0] < cfg.preprocess.min_obj_points: continue
        
        # For each resolution, sample the object point cloud and store it
        for pc_resolution in object_points.keys():
            obj_pcl = pcl_farthest_sample(obj_pcl, pc_resolution)
            object_points[pc_resolution].append(obj_pcl) # object_points[pc_resolution][i] is refererred to the i-th instance in the objects.json

        # if object_id == 154:
        #     pcd_2 = o3d.geometry.PointCloud()
        #     pcd_2.points = o3d.utility.Vector3dVector(object_points[256][-1])
        #     o3d.visualization.draw_geometries([pcd_2.paint_uniform_color([1, 0.706, 0]), axis])



    # Convert the lists to arrays for consistency
    for pc_resolution in object_points.keys():
        object_points[pc_resolution] = np.array(object_points[pc_resolution])

    # Return only the obj_points in a data_dict
    data_dict = {}
    data_dict['obj_points'] = object_points
    data_dict['ei'] = np.array(objectIDs) # list of the original IDs. data_dict['ei'][i] has the original ID of the pcd in data_dict['obj_points'][pc_resolution][i]

    return data_dict


with open(path_objData, 'r') as f:
    obj_data = json.load(f)

data_dict = get_data_dict(path_to_npy, obj_data, list_resolutions)



#
# Save the .pkl file
#

with open(path_save_pkl_file, 'wb') as f:  # 'wb' is write binary mode
    pickle.dump(data_dict, f)




end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
