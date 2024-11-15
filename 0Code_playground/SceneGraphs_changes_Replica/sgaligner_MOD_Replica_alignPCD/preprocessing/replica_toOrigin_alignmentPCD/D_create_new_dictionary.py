'''The new_data_dict that I want to get from this script is a replacement for the dataloader. This new_data_dict contains
information that are given from both the two scenes that are being compared.'''

import numpy as np
import torch
import pickle
import json


#
# Variables
#

# IMPORTANT: ref is the target, src is the source

path_to_pkl_ref = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/SGAligner_toOrigin/data_dict.pkl'
path_to_pkl_src = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/SGAligner_toOrigin/data_dict.pkl'
path_to_npy_src = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/SGAligner_toOrigin/data.npy'
pc_resolution = 4000
objectIDs_ref = [77, 93, 10, 4, 66, 59] # bike, bike, ceiling, sofa, mat, book
objectIDs_src = [34, 39, 27, 103, 38, 164] # bike, bike, ceiling, sofa, cup, sink
path_save_indexChanges = '/local/home/gmarsich/Desktop/data_Replica/index_changes_toOrigin.json'


#
# Computing the new_data_dict
#

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


# side function
def get_newObjectPoints(object_points, data_dict, objectIDs):
    ei_array = np.array(data_dict['ei'])
    positions = [np.where(ei_array == obj_id)[0] for obj_id in objectIDs]
    flat_positions = np.concatenate(positions)

    new_object_points = object_points[flat_positions]

    return new_object_points


# main function
def get_new_dictionary(path_to_pkl_src, path_to_pkl_ref, path_to_npy_src, pc_resolution, objectIDs_src, objectIDs_ref, path_save_indexChanges):
    
    new_data_dict = {}

    src_points = load_plydata_npy(path_to_npy_src, obj_ids = None)
    src_data_dict = load_pkl_data(path_to_pkl_src)
    ref_data_dict = load_pkl_data(path_to_pkl_ref)

    #
    # tot_obj_pts and tot_obj_count
    #

    pcl_center = np.mean(src_points, axis=0)

    src_object_points = src_data_dict['obj_points'][pc_resolution] - pcl_center
    ref_object_points = ref_data_dict['obj_points'][pc_resolution] - pcl_center

    new_src_object_points = get_newObjectPoints(src_object_points, src_data_dict, objectIDs_src) # new_src_object_points[i] contains the point cloud of ID objectIDs_src[i]
    new_ref_object_points = get_newObjectPoints(ref_object_points, ref_data_dict, objectIDs_ref)
    
    tot_object_points = torch.cat([torch.from_numpy(new_src_object_points), torch.from_numpy(new_ref_object_points)]).type(torch.FloatTensor)

    new_data_dict['tot_obj_pts'] = tot_object_points
    new_data_dict['tot_obj_count'] = tot_object_points.shape[0]

    #
    # graph_per_obj_count
    #

    new_data_dict['graph_per_obj_count'] = np.array([new_src_object_points.shape[0], new_ref_object_points.shape[0]])

    #
    # e1i and e2i + index_change.json
    #

    new_data_dict['e1i'] = np.array([x for x in range(len(new_src_object_points))])
    new_data_dict['e2i'] = np.array([x for x in range(len(new_ref_object_points))]) + new_src_object_points.shape[0]

    index_changes = {
    'src': [],
    'ref': []
    }

    for index, value in enumerate(objectIDs_src):
        index_changes['src'].append({
            'initialID': value,
            'finalID': int(new_data_dict['e1i'][index])
        })

    for index, value in enumerate(objectIDs_ref):
        index_changes['ref'].append({
            'initialID': value,
            'finalID': int(new_data_dict['e2i'][index])
        })


    with open(path_save_indexChanges, 'w') as json_file:
        json.dump(index_changes, json_file, indent=4)


    #
    # e1i_count and e2i_count
    #

    new_data_dict['e1i_count'] = len(new_src_object_points)
    new_data_dict['e2i_count'] = len(new_ref_object_points)

    return new_data_dict


#new_data_dict = get_new_dictionary(path_to_pkl_src, path_to_pkl_ref, path_to_npy_src, pc_resolution, objectIDs_src, objectIDs_ref)
