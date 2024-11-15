import argparse
import os 
import os.path as osp
import time
import numpy as np 

import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
sys.path.append('.')
sys.path.append('GeoTransformer')

from engine.single_tester import SingleTester
from utils import torch_util, scan3r
from aligner.sg_aligner import *
from configs import config, update_config
from utils import alignment, common, point_cloud
import preprocessing.replica_toOrigin_alignmentPCD.D_create_new_dictionary

class AlignerRegTester(SingleTester):
    def __init__(self, cfg, parser, new_data_dict):
        super().__init__(cfg, parser=parser)
        
        self.new_data_dict = new_data_dict

        self.run_reg = cfg.registration

        # Model Specific params
        self.modules = cfg.modules
        self.rel_dim = cfg.model.rel_dim
        self.attr_dim = cfg.model.attr_dim

        # # Metrics params
        # self.all_k = cfg.metrics.all_k
        # self.alignment_metrics_meter = {'mrr' : [], 'sgar' : {}}
        # for k in self.all_k:
        #     self.alignment_metrics_meter[k] = {'correct' : 0, 'total' : 0}
        
        # self.normal_registration_metrics_meter = {'CD' : [], 'IR' : [], 'RRE' : [], 'RTE' : [], 'recall' : [], 'FMR' : []}
        # self.aligner_registration_metrics_meter = {'CD' : [], 'IR' : [], 'RRE' : [], 'RTE' : [], 'recall' : [], 'FMR' : []}
        # self.recall_modes = ['2', '50', '100']
        # self.anchors = []
        # for recall_mode in self.recall_modes:
        #     self.alignment_metrics_meter['sgar'][recall_mode] = []

        # # dataloader
        # start_time = time.time()
        # loading_time = time.time() - start_time
        # message = f'Data loader created: {loading_time:.3f}s collapsed.'
        # self.logger.info(message)

        # model 
        model = self.create_model()
        self.register_model(model)
        self.model.eval()

        self.reg_k = cfg.reg_model.K


    def create_model(self):
        model = MultiModalEncoder(modules = self.modules, rel_dim = self.rel_dim, attr_dim=self.attr_dim).to(self.device) # GAIA had to modify the MultiModalEncoder
        message = 'Model created'
        self.logger.info(message)
        return model
    
    def test_step(self, data_dict):
        output_dict = self.model(data_dict)
        return output_dict
    
    # def print_metrics(self, results_dict):
    #     for key in results_dict.keys():
    #         if not self.run_reg and  'registration' in key: continue
    #         metrics_dict = self.compute_metrics(results_dict[key])
    #         message = common.get_log_string(result_dict=metrics_dict, name=key, timer=self.timer)
    #         self.logger.critical(message)

    # def compute_metrics(self, result_dict):
    #     metrics_dict = {}
    #     for key in result_dict:
    #         if type(key) == int:
    #             metrics_dict['hits@_{}'.format(key)] = round(result_dict[key]['correct'] / result_dict[key]['total'], 5)
    #         elif type(result_dict[key]) == list:
    #             metrics_dict[key] = round(np.array(result_dict[key]).mean(), 5)
    #         elif type(result_dict[key]) == dict: # sgar
    #             for mode in result_dict[key]:
    #                 metrics_dict[key + '_' + mode] = round(np.array(result_dict[key][mode]).mean(), 5)

    #     return metrics_dict
        
    def eval_step(self, data_dict, output_dict):
        data_dict = torch_util.release_cuda(data_dict)
        embedding = output_dict[self.modules[0]] # GAIA modified for my case, where I just have one module ('points')

        obj_cnt_start_idx = 0
        src_objects_count = data_dict['graph_per_obj_count'][0]
        
        obj_cnt_end_idx = data_dict['tot_obj_count']
        
        e1i_idxs = data_dict['e1i']
        e2i_idxs = data_dict['e2i']

        if e1i_idxs.shape[0] != 0 and e2i_idxs.shape[0] != 0:
            
            emb = embedding[obj_cnt_start_idx : obj_cnt_end_idx]

            emb = emb / emb.norm(dim=1)[:, None]
            sim = 1 - torch.mm(emb, emb.transpose(0,1))
            print(sim)
            print('\n')
            rank_list = torch.argsort(sim, dim = 1)
            print(rank_list)
            sorted_sim = torch.gather(sim, 1, rank_list)
            print(sorted_sim)
            assert np.max(e1i_idxs) <= rank_list.shape[0]

            node_corrs = alignment.compute_node_corrs(rank_list, src_objects_count, self.reg_k)
            print("\n\nASSOCIATIONS BETWEEN NODES")
            print(node_corrs)
            print("\n")
        
        return 
    


def parse_args(args_list=None): # GAIA modified parse_args
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', dest='config', default='', type=str, help='configuration file name')
    parser.add_argument('--snapshot', default=None, help='load from snapshot')
    parser.add_argument('--test_epoch', type=int, default=None, help='test epoch')
    parser.add_argument('--test_iter', type=int, default=None, help='test iteration')
    parser.add_argument('--reg_snapshot', default=None, help='load from snapshot')

    if args_list is not None:
        args = parser.parse_args(args_list)
    else:
        args = parser.parse_args()

    return parser, args


def main(): # GAIA modified main, but does not work properly (the snapshot is not carried in the right way in the code). Had to play a trick in a piece of code (src/engine/base_tester.py)
    args_list = [
        '--config', '/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/sgaligner_MOD_3RScan/configs/scan3r/scan3r_ground_truth.yaml',
        '--snapshot', '/local/home/gmarsich/Desktop/weights+files/point-epoch-50.pth.tar',
    ]

    parser, args = parse_args(args_list)
    cfg = update_config(config, args.config) # GAIA a variable containing the configs, basically

    path_to_pkl_ref = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/SGAligner_toOrigin_alignmentPCD/data_dict.pkl'
    path_to_pkl_src = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/SGAligner_toOrigin_alignmentPCD/data_dict.pkl'
    path_to_npy_src = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/SGAligner_toOrigin_alignmentPCD/data.npy'
    pc_resolution = 4000
    objectIDs_src = [34, 39, 27, 103, 38, 164] # 1: # bike, bike, ceiling, sofa, cup, sink
    objectIDs_ref = [77, 93, 10, 4, 66, 59] # 0: bike, bike, ceiling, sofa, mat, book
    
    path_save_indexChanges = '/local/home/gmarsich/Desktop/data_Replica/index_changes_toOrigin_alignmentPCD.json'

    new_data_dict = preprocessing.replica_toOrigin_alignmentPCD.D_create_new_dictionary.get_new_dictionary(path_to_pkl_src, path_to_pkl_ref, path_to_npy_src, pc_resolution, objectIDs_src, objectIDs_ref, path_save_indexChanges)
    tester = AlignerRegTester(cfg, parser, new_data_dict)
    tester.run()

if __name__ == '__main__':
    main()