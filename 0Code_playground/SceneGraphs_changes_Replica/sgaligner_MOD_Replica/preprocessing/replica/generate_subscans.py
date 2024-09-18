from tqdm import tqdm
import argparse
import random

import sys
sys.path.append('.')

from configs import config, update_config
from preprocessing.scan3r.subgenscan3r import SubGenScan3R

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', dest='config', default='', type=str, help='3R Scan configuration file name')
    parser.add_argument('--split', dest='split', default='', type=str, help='split to run on')
    
    args = parser.parse_args()
    return parser, args

if __name__ == '__main__':
    _, args = parse_args()
    cfg = update_config(config, args.config, ensure_dir=False)
    print('======== Replica .npy files generation : {} ========'.format(args.config))



    for idx in tqdm(range(len(sub_gen_scan3r))): # for idx in tqdm(range(1, 2)): # GAIA: with this it works!
        sub_gen_scan3r[idx, False]
    
    sub_gen_scan3r.calculate_overlap()
    sub_gen_scan3r.write_metadata()
