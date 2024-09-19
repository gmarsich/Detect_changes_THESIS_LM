'''preprocess.py but for Replica'''

import numpy as np
import os.path as osp
from utils import point_cloud
import argparse
import random
from configs import config, update_config


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', dest='config', default='', type=str, help='3R Scan configuration file name')
    parser.add_argument('--split', dest='split', default='train', type=str, help='split to run subscan generation on')
    parser.add_argument('--remove_nodes', dest='remove_node', default=False,  action='store_true', help='randomly remove nodes from scene graph')      
    parser.add_argument('--remove_edges', dest='remove_edge', default=False,  action='store_true', help='randomly remove edges from scene graph')   
    parser.add_argument('--change_node_semantic', dest='change_node_semantic', default=False,  action='store_true', help='randomly change semantic labels of nodes')        
    parser.add_argument('--change_edge_semantic', dest='change_edge_semantic', default=False,  action='store_true', help='randomly change semantic labels of edges')
    
    args = parser.parse_args()
    if args.remove_node:
        args.mode = 'node_removed'
    if args.remove_edge:
        args.mode = 'edge_removed'
    if args.change_node_semantic:
        args.mode = 'node_semantic_changed'
    if args.change_edge_semantic:
        args.mode = 'edge_semantic_changed'
    else:
        args.mode = 'orig'

    return parser, args


def get_data_dict(path_to_npy, obj_data, args, cfg):
    '''Get, for the dictionary:
        'obj_points' '''

    # Load the point cloud data from file (assumes ply_data contains 'x', 'y', 'z', 'objectId')
    ply_data = np.load(path_to_npy) # instead of osp.join(data_dir, 'scenes', scan_id, 'data.npy') I put path_to_npy
    points = np.stack([ply_data['x'], ply_data['y'], ply_data['z']]).transpose((1, 0))

    # Initialize the dictionary to store object points for different resolutions
    object_points = {}
    for pc_resolution in cfg.preprocess.pc_resolutions:
        object_points[pc_resolution] = []

    # Extract object data from obj_data
    object_data = obj_data['objects'] 

    # # Optionally remove some objects based on args
    # if args.remove_node:
    #     num_obj_to_keep = int(((100 - np.random.randint(15, 41)) / 100.0) * len(object_data))
    #     keep_obj_indices = np.random.choice(len(object_data), num_obj_to_keep, replace=False)
    #     object_data = [object_data[idx] for idx in keep_obj_indices]
    
    # # Optionally change some object semantics
    # if args.change_node_semantic:
    #     num_obj_to_change = int((np.random.randint(15, 41) / 100.0) * len(object_data))
    #     change_obj_indices = np.random.choice(len(object_data), num_obj_to_change, replace=False)
    #     orig_objects_ids = []

    #     for idx, object in enumerate(object_data):
    #         orig_objects_ids.append(int(object['id'])) 

    # Iterate through each object to collect point cloud data
    for idx, object in enumerate(object_data):
        # if not cfg.use_predicted : attribute = [item for sublist in object['attributes'].values() for item in sublist]

        object_id = int(object['id'])
        # object_id_for_pcl = int(object['id'])
        
        # # Change object semantic if required
        # if args.change_node_semantic and idx in change_obj_indices:
        #     object_id_for_pcl = np.random.choice(orig_objects_ids)
        #     while object_id_for_pcl == int(object['id']):
        #         object_id_for_pcl = np.random.choice(orig_objects_ids)

        # Get the points belonging to the current object
        obj_pt_idx = np.where(ply_data['objectId'] == object_id)
        obj_pcl = points[obj_pt_idx]

        # Skip objects with fewer points than the minimum required
        if obj_pcl.shape[0] < cfg.preprocess.min_obj_points: continue
        
        # For each resolution, sample the object point cloud and store it
        for pc_resolution in object_points.keys():
            obj_pcl = point_cloud.pcl_farthest_sample(obj_pcl, pc_resolution)
            object_points[pc_resolution].append(obj_pcl)

    # Convert the lists to arrays for consistency
    for pc_resolution in object_points.keys():
        object_points[pc_resolution] = np.array(object_points[pc_resolution])

    # Return only the obj_points in a data_dict
    data_dict = {}
    data_dict['obj_points'] = object_points

    return data_dict



if __name__ == '__main__':

    _, args = parse_args()
    cfg = update_config(config, args.config, ensure_dir=False)
    random.seed(cfg.seed)

    path_to_npy = '' # TODO
    data_dict = get_data_dict(path_to_npy, obj_data, args, cfg)
