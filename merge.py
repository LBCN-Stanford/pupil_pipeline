import sys
from params import save_params, get_params
from misc import select_folder, load_pkl, save_pkl, make_path
from epoch import Epoched
from plot import plot_conds
import os
import numpy as np
import warnings
import scipy.io as spio

def merge(gather_dir=os.getcwd(), combine_type='run', base_name='',
          out_dir='', **params):

    """
    Merges the epoched*.pkl objects in gather_dir
    Arguments:
        gather_dir: path to folder containing epoched files
        combine_type: 'run' to combine averages of each run
                      'trial' to combine every trial
    Outputs:
        merged.pkl, merged.mat
    """
    files = [f for f in os.listdir(gather_dir) if 'pkl' in f and 'epoched' in f]
    merged = None
    for f in files:
        run = load_pkl(os.path.join(gather_dir, f))
        if merged is None:
            merged = Epoched(run.n_categs, run.n_samples, 0)
            merged.names = run.names

        if combine_type == 'run':
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                avg = np.nanmean(run.matrix, axis=2, keepdims=True)
            merged.matrix = np.concatenate((merged.matrix, avg), axis=2)
        elif combine_type == 'trial':
            merged.matrix = np.concatenate((merged.matrix, run.matrix), axis=2)

    spio.savemat(make_path('merged', '.mat', out_dir=out_dir,
                           base_name=base_name), {'merged': merged})
    save_pkl(make_path('merged', '.pkl', out_dir=out_dir,
                       base_name=base_name), merged)
    plot_conds(merged, **params)



#TODO set the new params and read them...
if __name__ == '__main__':
    params = get_params(sys.argv)

    #TODO for testing purposes, delete it later.
    params["gather_dir"] = select_folder()
    params["out_dir"] = params["gather_dir"]

    params["base_name"] = os.path.basename(os.path.normpath(params["gather_dir"]))
    merge(**params)
    save_params(params)
