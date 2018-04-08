import sys
from params import save_params, get_params
from misc import select_folder, load_pkl
from readpupil import read_pupil
from epoch import epoch, Epoched
from plot import plot_conds
import time
import os

def merge(gather_dir=os.getcwd(), **params):
    files = [f for f in os.listdir(gather_dir) if 'pkl' in f]
    first = load_pkl(os.path.join(gather_dir, files[0]))
    merged = Epoched(first.n_categs, first.n_samples, len(files))
    for f in files:
        run = load_pkl(os.path.join(gather_dir, f))
        if merged is None: merged = Epoched(run.n_categs,
                                            run.n_samples, len(files))


#TODO set the new params and read them...
if __name__ == '__main__':
    params = get_params(sys.argv)

    #TODO for testing purposes, delete it later.
    # params["gather_dir"] = select_folder()
    params["gather_dir"] = "/home/harrysha/Dropbox/data/S18_120/Gathered/"


    params["base_name"] = os.path.basename(os.path.normpath(params["gather_dir"]))
    merge(**params)
    save_params(params)
