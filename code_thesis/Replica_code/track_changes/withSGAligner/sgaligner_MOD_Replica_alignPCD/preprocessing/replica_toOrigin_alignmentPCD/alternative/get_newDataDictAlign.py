import torch



new_data_dict  = {}
tot_object_points = torch.cat([torch.from_numpy(new_src_object_points), torch.from_numpy(new_ref_object_points)]).type(torch.FloatTensor)

new_data_dict['tot_obj_pts'] = tot_object_points


