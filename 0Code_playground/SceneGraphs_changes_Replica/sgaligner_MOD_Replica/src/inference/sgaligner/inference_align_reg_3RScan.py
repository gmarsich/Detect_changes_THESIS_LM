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
# from engine.registration_evaluator import RegistrationEvaluator # TODO
from utils import torch_util, scan3r
from aligner.sg_aligner import *
from datasets.loaders import get_val_dataloader
#from datasets.loaders import get_val_dataloader_Replica
from configs import config, update_config
from utils import alignment, common, point_cloud
# from GeoTransformer.config import make_cfg as make_cfg_reg # GAIA seems not to be useful in this code

class AlignerRegTester(SingleTester):
    def __init__(self, cfg, parser):
        super().__init__(cfg, parser=parser)
        
        self.run_reg = cfg.registration

        # Model Specific params
        self.modules = cfg.modules
        self.rel_dim = cfg.model.rel_dim
        self.attr_dim = cfg.model.attr_dim

        # Metrics params
        self.all_k = cfg.metrics.all_k
        self.alignment_metrics_meter = {'mrr' : [], 'sgar' : {}}
        for k in self.all_k:
            self.alignment_metrics_meter[k] = {'correct' : 0, 'total' : 0}
        
        self.normal_registration_metrics_meter = {'CD' : [], 'IR' : [], 'RRE' : [], 'RTE' : [], 'recall' : [], 'FMR' : []}
        self.aligner_registration_metrics_meter = {'CD' : [], 'IR' : [], 'RRE' : [], 'RTE' : [], 'recall' : [], 'FMR' : []}
        self.recall_modes = ['2', '50', '100']
        self.anchors = []
        for recall_mode in self.recall_modes:
            self.alignment_metrics_meter['sgar'][recall_mode] = []

        # dataloader
        start_time = time.time()
        dataset, data_loader = get_val_dataloader(cfg) # GAIA data_loader will become test_loader
        #dataset, data_loader = get_val_dataloader_Replica(cfg) # GAIA TODO data_loader will become test_loader
        loading_time = time.time() - start_time
        message = f'Data loader created: {loading_time:.3f}s collapsed.'
        self.logger.info(message)

        self.register_loader(data_loader) # GAIA to change. It sets test_loader
        #self.register_dataset(dataset) # GAIA: it seems that we don't need this

        # model 
        model = self.create_model()
        self.register_model(model)
        self.model.eval()

        # Registration
        # BEGINNING if
        self.reg_k = cfg.reg_model.K
        #reg_snapshot = self.args.reg_snapshot
        #self.registration_evaluator = RegistrationEvaluator(self.device, cfg, reg_snapshot, self.logger, visualise_registration=True)
        #self.visualise_registration = True
        # END if

    def create_model(self):
        model = MultiModalEncoder(modules = self.modules, rel_dim = self.rel_dim, attr_dim=self.attr_dim).to(self.device) # GAIA had to modify the MultiModalEncoder
        message = 'Model created'
        self.logger.info(message)
        return model
    
    def test_step(self, iteration, data_dict):
        output_dict = self.model(data_dict)
        return output_dict
    
    def print_metrics(self, results_dict):
        for key in results_dict.keys():
            if not self.run_reg and  'registration' in key: continue
            metrics_dict = self.compute_metrics(results_dict[key])
            message = common.get_log_string(result_dict=metrics_dict, name=key, timer=self.timer)
            self.logger.critical(message)

    def compute_metrics(self, result_dict):
        metrics_dict = {}
        for key in result_dict:
            if type(key) == int:
                metrics_dict['hits@_{}'.format(key)] = round(result_dict[key]['correct'] / result_dict[key]['total'], 5)
            elif type(result_dict[key]) == list:
                metrics_dict[key] = round(np.array(result_dict[key]).mean(), 5)
            elif type(result_dict[key]) == dict: # sgar
                for mode in result_dict[key]:
                    metrics_dict[key + '_' + mode] = round(np.array(result_dict[key][mode]).mean(), 5)

        return metrics_dict
        
    def eval_step(self, iteration, data_dict, output_dict):
        data_dict = torch_util.release_cuda(data_dict)
        embedding = output_dict[self.modules[0]] # GAIA modified for my case, where I just have one module ('points')

        e1i_start_idx = 0
        e2i_start_idx = 0
        obj_cnt_start_idx = 0
        #curr_total_objects_count = 0 

        batch_idx = 0 # GAIA: I removed the for loop  

        # GAIA: modified (no for loop: for batch_idx in range(self.test_loader.batch_size)) because we just have one iteration

        src_objects_count = data_dict['graph_per_obj_count'][batch_idx][0]
        # ref_objects_count = data_dict['graph_per_obj_count'][batch_idx][1]
        # pcl_center = data_dict['pcl_center'][batch_idx]
        
        #all_objects_ids = data_dict['obj_ids']
        e1i_end_idx = e1i_start_idx + data_dict['e1i_count'][batch_idx]
        e2i_end_idx = e2i_start_idx + data_dict['e2i_count'][batch_idx]
        obj_cnt_end_idx = obj_cnt_start_idx + data_dict['tot_obj_count'][batch_idx]

        e1i_idxs = data_dict['e1i'][e1i_start_idx : e1i_end_idx]
        e2i_idxs = data_dict['e2i'][e2i_start_idx : e2i_end_idx]
        # e1i_idxs -= curr_total_objects_count
        # e2i_idxs -= curr_total_objects_count

        if e1i_idxs.shape[0] != 0 and e2i_idxs.shape[0] != 0:
            #assert e1i_idxs.shape == e2i_idxs.shape
            
            emb = embedding[obj_cnt_start_idx : obj_cnt_end_idx]
            emb = emb / emb.norm(dim=1)[:, None]
            sim = 1 - torch.mm(emb, emb.transpose(0,1))
            rank_list = torch.argsort(sim, dim = 1)
            assert np.max(e1i_idxs) <= rank_list.shape[0]


            # BEGINNING OF if
            node_corrs = alignment.compute_node_corrs(rank_list, src_objects_count, self.reg_k)
            print("\n\nASSOCIATIONS BETWEEN NODES")
            print(node_corrs)
            print("\n")
            # node_corrs = alignment.get_node_corrs_objects_ids(node_corrs, all_objects_ids, curr_total_objects_count) # GAIA: "global IDs"
        
        return 
        # GAIA: the return was: { 'alignment_metrics' : self.alignment_metrics_meter, 'normal_registration_metrics' : self.normal_registration_metrics_meter, 'aligner_registration_metrics' : self.aligner_registration_metrics_meter }
        



    def eval_step_Replica(self, data_dict, output_dict):
        data_dict = torch_util.release_cuda(data_dict)
        embedding = output_dict[self.modules[0]] # GAIA modified for my case, where I just have one module ('points')

        e1i_start_idx = 0
        e2i_start_idx = 0
        obj_cnt_start_idx = 0
        #curr_total_objects_count = 0 

        batch_idx = 0 # GAIA: I removed the for loop  

        # GAIA: modified (no for loop: for batch_idx in range(self.test_loader.batch_size)) because we just have one iteration

        src_objects_count = data_dict['graph_per_obj_count'][batch_idx][0]
        # ref_objects_count = data_dict['graph_per_obj_count'][batch_idx][1]
        # pcl_center = data_dict['pcl_center'][batch_idx]
        
        #all_objects_ids = data_dict['obj_ids']
        e1i_end_idx = e1i_start_idx + data_dict['e1i_count'][batch_idx]
        e2i_end_idx = e2i_start_idx + data_dict['e2i_count'][batch_idx]
        obj_cnt_end_idx = obj_cnt_start_idx + data_dict['tot_obj_count'][batch_idx]

        e1i_idxs = data_dict['e1i'][e1i_start_idx : e1i_end_idx]
        e2i_idxs = data_dict['e2i'][e2i_start_idx : e2i_end_idx]
        # e1i_idxs -= curr_total_objects_count
        # e2i_idxs -= curr_total_objects_count

        if e1i_idxs.shape[0] != 0 and e2i_idxs.shape[0] != 0:
            #assert e1i_idxs.shape == e2i_idxs.shape
            
            emb = embedding[obj_cnt_start_idx : obj_cnt_end_idx]
            emb = emb / emb.norm(dim=1)[:, None]
            sim = 1 - torch.mm(emb, emb.transpose(0,1))
            rank_list = torch.argsort(sim, dim = 1)
            assert np.max(e1i_idxs) <= rank_list.shape[0]


            # BEGINNING OF if
            node_corrs = alignment.compute_node_corrs(rank_list, src_objects_count, self.reg_k)
            print("\n\nASSOCIATIONS BETWEEN NODES")
            print(node_corrs)
            print("\n")
            # node_corrs = alignment.get_node_corrs_objects_ids(node_corrs, all_objects_ids, curr_total_objects_count) # GAIA: "global IDs"
        
        return 



# def parse_args(parser=None):
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--config', dest='config', default='', type=str, help='configuration file name')
#     parser.add_argument('--snapshot', default=None, help='load from snapshot')
#     parser.add_argument('--test_epoch', type=int, default=None, help='test epoch')
#     parser.add_argument('--test_iter', type=int, default=None, help='test iteration')
#     parser.add_argument('--reg_snapshot', default=None, help='load from snapshot')

#     args = parser.parse_args()
#     return parser, args


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

# def main():
#     parser, args = parse_args()
#     cfg = update_config(config, args.config)

#     tester = AlignerRegTester(cfg, parser)
#     tester.run()

def main(): # GAIA modified main, but does not work properly (the snapshot is not carried in the right way in the code). Had to play a trick in a piece of code (src/engine/base_tester.py)
    args_list = [
        '--config', '/local/home/gmarsich/Desktop/Thesis/0Code_playground/SceneGraphs_changes_Replica/sgaligner_MOD_3RScan/configs/scan3r/scan3r_ground_truth.yaml',
        '--snapshot', '/local/home/gmarsich/Desktop/weights+files/point-epoch-50.pth.tar',
        # '--test_epoch', '10',
        # '--test_iter', '1000',
        # '--reg_snapshot', 'path/to/reg_snapshot'
    ]

    parser, args = parse_args(args_list)
    cfg = update_config(config, args.config) # GAIA a variable containing the configs, basically

    tester = AlignerRegTester(cfg, parser)
    tester.run()

if __name__ == '__main__':
    main()

    # [(0, 8), (1, 9), (3, 10), (4, 11), (5, 12), (6, 13), (7, 8)]