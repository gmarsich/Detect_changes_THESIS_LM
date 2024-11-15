from typing import Dict
import torch
import ipdb
import numpy as np
from tqdm import tqdm

from engine.base_tester import BaseTester
from utils import torch_util
from utils.common import get_log_string

class SingleTester(BaseTester):
    def __init__(self, cfg, parser=None, cudnn_deterministic=True):
        super().__init__(cfg, parser=parser, cudnn_deterministic=cudnn_deterministic)

    def before_test_epoch(self):
        pass

    def before_test_step(self, iteration, data_dict):
        pass

    def test_step(self, iteration, data_dict) -> Dict:
        pass

    def eval_step(self, iteration, data_dict, output_dict) -> Dict:
        pass

    def after_test_step(self, iteration, data_dict, output_dict, result_dict):
        pass

    def after_test_epoch(self):
        pass

    def summary_string(self, iteration, data_dict, output_dict, result_dict):
        return get_log_string(result_dict)

    def run(self):
        assert self.test_loader is not None
        self.load_snapshot(self.args.snapshot)
        self.model.eval()
        torch.set_grad_enabled(False)
        #self.before_test_epoch() # GAIA it seems not to do anything
        total_iterations = len(self.test_loader)
        pbar = tqdm(enumerate(self.test_loader), total=total_iterations) # GAIA __getitem__ function is used to get data_dict; 
        for iteration, data_dict in pbar: # GAIA: the for loop is executed just once!
            # on start
            self.iteration = iteration + 1
            data_dict = torch_util.to_cuda(data_dict)
            #self.before_test_step(self.iteration, data_dict) # GAIA it seems not to do anything
            # test step
            torch.cuda.synchronize()
            #self.timer.add_prepare_time()
            output_dict = self.test_step(self.iteration, data_dict) # GAIA the output, given by the model, is a set of embeddings 
            torch.cuda.synchronize()
            #self.timer.add_process_time()
            # eval step. GAIA: modified from the original
            self.eval_step(self.iteration, data_dict, output_dict) # GAIA core function, where results are computed; "original" data and embeddings are both used
            #message = f'{self.timer.tostring()}'
            #pbar.set_description(message)
            torch.cuda.empty_cache()
        
        #self.after_test_epoch()

        #self.print_metrics(results_dict)

