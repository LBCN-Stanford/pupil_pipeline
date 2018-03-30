import sys
from params import save_params, get_params
from misc import select_files, folder_setup, get_files
from qualitycheck import qualitycheck
from readpupil import read_pupil
from preprocess import preprocess
from epoch import epoch
from plot import plot_conds
import time

if __name__ == '__main__':

    params = get_params(sys.argv)
    eye_paths, events_path = get_files(**params)
    assert len(eye_paths) == len(
        events_path), 'You must select the same number of pupil and event files.'

    t0 = time.time()
    for eye_path, events_path in zip(eye_paths, events_path):
        folder_setup(eye_path, params)
        pupil_data = read_pupil(eye_path)
        qualitycheck(pupil_data, **params)
        preprocess(pupil_data, **params)
        epoched = epoch(pupil_data, events_path, **params)
        plot_conds(epoched, **params)
        save_params(params)

    print('\nDone!\n')
    print('\n\nIn total, that took {} seconds!'.format(time.time() - t0))
