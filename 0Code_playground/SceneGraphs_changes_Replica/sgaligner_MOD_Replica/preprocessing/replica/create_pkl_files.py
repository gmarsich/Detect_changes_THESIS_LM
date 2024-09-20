'''preprocess.py but for Replica.
Given a scene, the .pkl file will be created.'''

import numpy as np

import sys
sys.path.append('.')


from utils import point_cloud
import random
from configs import config, update_config


#
# Variables
#

path_to_npy = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/SGAligner/data.npy'
obj_data = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/SGAligner/objects.json'
path_config = '/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/sgaligner_MOD_3RScan/configs/scan3r/scan3r_ground_truth.yaml'


#
# Get the .pkl file
#

def get_data_dict(path_to_npy, obj_data, cfg):
    '''Get, for the dictionary:
        'obj_points' # something like: object_points[pc_resolution][i], and contains a point cloud
        'ei' # indeces of the instances in the scene
    '''

    # Load the point cloud data from file (assumes ply_data contains 'x', 'y', 'z', 'objectId')
    ply_data = np.load(path_to_npy)
    points = np.stack([ply_data['x'], ply_data['y'], ply_data['z']]).transpose((1, 0))
    objectIDs = ply_data['objectId'] # something like array([0, 1, 2, 3])

    # Initialize the dictionary to store object points for different resolutions
    object_points = {}
    for pc_resolution in cfg.preprocess.pc_resolutions:
        object_points[pc_resolution] = []

    # Extract object data from obj_data
    object_data = obj_data['objects'] # obj_data['objects'][0] is the first dictionary, with info on a specific instance

    # Iterate through each object to collect point cloud data
    for idx, object in enumerate(object_data):

        object_id = int(object['id'])

        # Get the points belonging to the current object
        obj_pt_idx = np.where(ply_data['objectId'] == object_id) # indeces of the points in the pcd corresponding to a specific ID
        obj_pcl = points[obj_pt_idx] # array with points of the pcd of a specific instance

        # Skip objects with fewer points than the minimum required
        # if obj_pcl.shape[0] < cfg.preprocess.min_obj_points: continue
        
        # For each resolution, sample the object point cloud and store it
        for pc_resolution in object_points.keys():
            obj_pcl = point_cloud.pcl_farthest_sample(obj_pcl, pc_resolution)
            object_points[pc_resolution].append(obj_pcl) # object_points[pc_resolution][i] is refererred to the i-th instance in the objects.json

    # Convert the lists to arrays for consistency
    for pc_resolution in object_points.keys():
        object_points[pc_resolution] = np.array(object_points[pc_resolution])

    # Return only the obj_points in a data_dict
    data_dict = {}
    data_dict['obj_points'] = object_points
    data_dict['ei'] = objectIDs

    return data_dict



cfg = update_config(config, path_config, ensure_dir=False)
random.seed(cfg.seed)

data_dict = get_data_dict(path_to_npy, obj_data, cfg)
