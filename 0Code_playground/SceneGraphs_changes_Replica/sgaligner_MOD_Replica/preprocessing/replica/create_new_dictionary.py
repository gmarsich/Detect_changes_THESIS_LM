'''The new_data_dict that I want to get from this script is a replacement for the dataloader. This new_data_dict contains
information that are given from both the two scenes that are being compared.'''

import numpy as np
import torch
import pickle

# side function
def load_plydata_npy(file_path, obj_ids = None, return_ply_data = False):
    ply_data = np.load(file_path)
    points =  np.stack([ply_data['x'], ply_data['y'], ply_data['z']]).transpose((1, 0))

    if obj_ids is not None:
        if type(obj_ids) == np.ndarray:
            obj_ids_pc = ply_data['objectId']
            obj_ids_pc_mask = np.isin(obj_ids_pc, obj_ids)
            points = points[np.where(obj_ids_pc_mask == True)[0]]
        else:
            obj_ids_pc = ply_data['objectId']
            points = points[np.where(obj_ids_pc == obj_ids)[0]]
    
    if return_ply_data: return points, ply_data
    else: return points


# side function
def load_pkl_data(filename):
    with open(filename, 'rb') as handle:
        data_dict = pickle.load(handle)
    return data_dict


# main function
def get_new_dictionary(path_to_pkl_src, path_to_pkl_ref, path_to_npy_src, pc_resolution):
    '''Get, for the new dictionary:
        'tot_obj_pts'
        'graph_per_obj_count' '''
    
    new_data_dict = {}

    #
    # tot_obj_pts
    #

    src_points = load_plydata_npy(path_to_npy_src, obj_ids = None)
    src_data_dict = load_pkl_data(path_to_pkl_src)
    ref_data_dict = load_pkl_data(path_to_pkl_ref)

    pcl_center = np.mean(src_points, axis=0)

    src_object_points = src_data_dict['obj_points'][pc_resolution] - pcl_center
    ref_object_points = ref_data_dict['obj_points'][pc_resolution] - pcl_center
    
    tot_object_points = torch.cat([torch.from_numpy(src_object_points), torch.from_numpy(ref_object_points)]).type(torch.FloatTensor)


    new_data_dict['tot_obj_pts'] = tot_object_points



    #
    # graph_per_obj_count
    #

    new_data_dict['graph_per_obj_count'] = np.array([src_object_points.shape[0], ref_object_points.shape[0]])



    return new_data_dict