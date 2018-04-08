import sys
from params import save_params, get_params
from misc import folder_setup, get_files
from qualitycheck import qualitycheck
from readpupil import read_pupil
from preprocess import preprocess
from epoch import epoch
from plot import plot_conds
import time
import os

def merge(folder):
    pass

#TODO set the new params and read them...
if __name__ == '__main__':
    params = get_params(sys.argv)
    params[out_dir] = sys.argv[2]
    params[base_name] = os.path.basename(os.path.normpath(sys.argv[2]))
    merge(argv[1])
    save_params(params)
